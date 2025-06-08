from common.cache import CacheManagement, RateLimit
from django.conf import settings
from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from user.models import User

from .serializers import PhoneNumberSerializer, VerifyOTPSerializer
from .services import cache_otp, generate_otp, send_otp_sms


class RequestOTPView(APIView):
    @extend_schema(
        summary="Request OTP for Phone Number Authentication",
        description=(
            "Sends a One-Time Password (OTP) to the provided phone number "
            "for user authentication. If the user does not exist, a new "
            "inactive user account will be created."
        ),
        tags=["Authentication"],  # Best practice: Group related endpoints
        request=PhoneNumberSerializer,
        responses={
            200: OpenApiResponse(
                description="OTP sent successfully.",
                response=dict,  # Use `dict` for simple inline object or define a schema
                examples=[
                    OpenApiExample(
                        'Success Response',
                        value={"message": "OTP sent successfully"},
                        response_only=True,
                        status_codes=["200"],
                    )
                ],
            ),
            400: OpenApiResponse(
                description="Invalid input or missing phone number.",
                # Assuming PhoneNumberSerializer handles validation errors
                response=dict,  # Or define a generic ErrorSchema
                examples=[
                    OpenApiExample(
                        'Invalid Phone Number',
                        value={"phone_number": ["Enter a valid phone number."]},
                        response_only=True,
                        status_codes=["400"],
                    )
                ],
            ),
            429: OpenApiResponse(
                description="Too many requests. Rate limit exceeded for this phone number.",
                response=dict,
                examples=[
                    OpenApiExample(
                        'Rate Limit Exceeded',
                        value={
                            "detail": "Request was throttled. Expected available in 30 seconds."
                        },
                        response_only=True,
                        status_codes=["429"],
                    )
                ],
            ),
            500: OpenApiResponse(
                description="Internal Server Error: Failed to send OTP.",
                response=dict,
                examples=[
                    OpenApiExample(
                        'SMS Send Failure',
                        value={"error": "Failed to send OTP"},
                        response_only=True,
                        status_codes=["500"],
                    )
                ],
            ),
        },
    )
    @RateLimit(
        rate=settings.RATELIMIT_USER_RATE,
        window=settings.RATELIMIT_USER_WINDOW,
        freeze=settings.RATELIMIT_USER_FREEZE,
    )
    def post(self, request):
        serializer = PhoneNumberSerializer(data=request.data)
        if not serializer.is_valid():
            errors = serializer.errors
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        phone_number = serializer.validated_data['phone_number']

        # Create user if doesn't exist
        user, created = User.objects.get_or_create(phone_number=phone_number)
        if created:
            user.is_active = False
            user.save()

        # Generate and cache OTP
        otp = generate_otp()
        cache_otp(phone_number, otp)

        # Send OTP via SMS
        if not send_otp_sms(phone_number, otp):
            error_msg = {"error": "Failed to send OTP"}
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return Response(error_msg, status=status_code)

        return Response(
            {"message": "OTP sent successfully"},
            status=status.HTTP_200_OK,
        )


class VerifyOTPView(APIView):
    @extend_schema(
        summary="Verify OTP and Authenticate User",
        description=(
            "Verifies the provided One-Time Password (OTP) for the given phone number. "
            "On successful verification, activates the user account (if inactive) "
            "and returns JWT access and refresh tokens for subsequent authenticated requests."
        ),
        tags=["Authentication"],  # Best practice: Group related endpoints
        request=VerifyOTPSerializer,
        responses={
            200: OpenApiResponse(
                description="Authentication successful. Returns JWT tokens.",
                # Define a schema for the successful response payload
                response={
                    "type": "object",
                    "properties": {
                        "access": {"type": "string", "description": "JWT Access Token"},
                        "refresh": {
                            "type": "string",
                            "description": "JWT Refresh Token",
                        },
                        "user_id": {
                            "type": "integer",
                            "description": "ID of the authenticated user",
                        },
                        "phone_number": {
                            "type": "string",
                            "description": "Phone number of the authenticated user",
                        },
                    },
                    "required": ["access", "refresh", "user_id", "phone_number"],
                },
                examples=[
                    OpenApiExample(
                        'Successful Authentication',
                        value={
                            "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                            "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                            "user_id": 1,
                            "phone_number": "+1234567890",
                        },
                        response_only=True,
                        status_codes=["200"],
                    )
                ],
            ),
            400: OpenApiResponse(
                description="Invalid input or incorrect OTP.",
                response=dict,  # Or define a generic ErrorSchema
                examples=[
                    OpenApiExample(
                        'Invalid OTP',
                        value={"error": "Invalid OTP"},
                        response_only=True,
                        status_codes=["400"],
                    ),
                    OpenApiExample(
                        'Validation Errors',
                        value={
                            "phone_number": ["This field is required."],
                            "otp": ["This field is required."],
                        },
                        response_only=True,
                        status_codes=["400"],
                    ),
                ],
            ),
        },
    )
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        phone_number = serializer.validated_data['phone_number']
        otp = serializer.validated_data['otp']

        # Get cached OTP
        cache = CacheManagement()
        cached_otp = cache.get_key(f"otp:{phone_number}")

        if not cached_otp or cached_otp != otp:
            error_msg = {"error": "Invalid OTP"}
            status_code = status.HTTP_400_BAD_REQUEST
            return Response(error_msg, status=status_code)

        # Get user
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            # This case might happen if OTP was requested, but user was somehow deleted before verification.
            # Or if an invalid phone number is sent to verify.
            error_msg = {"error": "User not found for this phone number."}
            return Response(error_msg, status=status.HTTP_400_BAD_REQUEST)

        # Activate user
        user.is_active = True
        user.save()

        # Generate JWT token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response(
            {
                "access": access_token,
                "refresh": str(refresh),
                "user_id": user.id,
                "phone_number": user.phone_number,
            },
            status=status.HTTP_200_OK,
        )

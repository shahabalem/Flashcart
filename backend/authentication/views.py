from common.cache import CacheManagement, RateLimit
from django.conf import settings
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from user.models import User

from .serializers import PhoneNumberSerializer, VerifyOTPSerializer
from .services import cache_otp, generate_otp, send_otp_sms


class RequestOTPView(APIView):
    @extend_schema(
        request=PhoneNumberSerializer,
        responses={
            200: OpenApiResponse(description="OTP sent successfully"),
            400: OpenApiResponse(description="Invalid input"),
            429: OpenApiResponse(description="Too many requests"),
            500: OpenApiResponse(description="Failed to send OTP"),
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
        request=VerifyOTPSerializer,
        responses={
            200: OpenApiResponse(description="Authentication successful"),
            400: OpenApiResponse(description="Invalid input or OTP"),
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
        user = User.objects.get(phone_number=phone_number)

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

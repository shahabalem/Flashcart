from rest_framework import serializers
from user.models import User


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)


class VerifyOTPSerializer(PhoneNumberSerializer):
    otp = serializers.CharField(max_length=6)


class UserActivationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_active']

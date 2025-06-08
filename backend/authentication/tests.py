from unittest.mock import patch

from common.cache.redis_cache import CacheManagement
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from user.models import User


class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.request_otp_url = reverse('request_otp')
        self.verify_otp_url = reverse('verify_otp')
        self.phone_number = '+989123456789'
        self.valid_otp = '123456'
        self.cache = CacheManagement()

    def tearDown(self):
        # Clear cache after each test
        self.cache.remove_key(f'otp:{self.phone_number}')

    @patch('authentication.services.send_otp_sms')
    def test_request_otp_success(self, mock_send_otp):
        mock_send_otp.return_value = True

        # Test new user creation
        response = self.client.post(
            self.request_otp_url,
            {'phone_number': self.phone_number},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            User.objects.filter(phone_number=self.phone_number).exists(),
        )

        # Test existing user
        response = self.client.post(
            self.request_otp_url,
            {'phone_number': self.phone_number},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify OTP was cached
        cached_otp = self.cache.get_key(f'otp:{self.phone_number}')
        self.assertIsNotNone(cached_otp)
        self.assertEqual(len(cached_otp), 6)

    def test_request_otp_invalid_phone(self):
        response = self.client.post(
            self.request_otp_url, {'phone_number': 'invalid'}, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('phone_number', response.data)

    @patch('authentication.services.send_otp_sms')
    def test_request_otp_sms_failure(self, mock_send_otp):
        mock_send_otp.return_value = False

        response = self.client.post(
            self.request_otp_url,
            {'phone_number': self.phone_number},
            format='json',
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    @patch('authentication.services.send_otp_sms')
    def test_verify_otp_success(self, mock_send_otp):
        mock_send_otp.return_value = True

        # First request OTP to create user and cache OTP
        self.client.post(
            self.request_otp_url,
            {'phone_number': self.phone_number},
        )

        # Verify with correct OTP
        self.cache.set_key(f'otp:{self.phone_number}', self.valid_otp, 120)
        response = self.client.post(
            self.verify_otp_url,
            {'phone_number': self.phone_number, 'otp': self.valid_otp},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

        # Verify user is activated
        user = User.objects.get(phone_number=self.phone_number)
        self.assertTrue(user.is_active)

    def test_verify_otp_invalid(self):
        # Test with invalid OTP
        response = self.client.post(
            self.verify_otp_url,
            {'phone_number': self.phone_number, 'otp': 'wrong'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_verify_otp_expired(self):
        # Set OTP with very short TTL
        self.cache.set_key(f'otp:{self.phone_number}', self.valid_otp, 1)

        # Wait for OTP to expire
        import time

        time.sleep(1)

        response = self.client.post(
            self.verify_otp_url,
            {'phone_number': self.phone_number, 'otp': self.valid_otp},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_verify_otp_without_request(self):
        # Verify without requesting OTP first
        response = self.client.post(
            self.verify_otp_url,
            {'phone_number': self.phone_number, 'otp': self.valid_otp},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

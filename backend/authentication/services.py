import logging
import random

from common.cache.redis_cache import CacheManagement
from django.conf import settings
from kavenegar import APIException, HTTPException, KavenegarAPI

logger = logging.getLogger(__name__)
cache = CacheManagement()


def generate_otp(length=6):
    """Generate a random numeric OTP of specified length"""
    return ''.join(random.choices('0123456789', k=length))


def cache_otp(phone_number, otp, ttl=120):
    """Cache OTP in Redis with phone number as key"""
    key = f"otp:{phone_number}"
    cache.set_key(key, otp, ttl)
    return True


def send_otp_sms(phone_number, otp):
    """Send OTP via Kaveh Negar SMS service"""
    if not hasattr(settings, 'KAVEH_NEGAR_API_KEY'):
        raise ValueError("Kaveh Negar API key not configured")

    try:
        api = KavenegarAPI(settings.KAVEH_NEGAR_API_KEY)
        params = {
            'sender': '',  # Use default sender
            'receptor': phone_number,
            'message': f'Your verification code is: {otp}',
        }
        response = api.sms_send(params)
        logger.info(f"OTP sent to {phone_number}: {response}")
        return True
    except (APIException, HTTPException) as e:
        logger.error(f"Kaveh Negar API error: {e}")
        return False

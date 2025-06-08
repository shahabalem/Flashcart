import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class KavenegarService:
    """
    Service for sending SMS via Kavenegar API
    Docs: https://kavenegar.com/rest.html
    """

    @staticmethod
    def send_sms(phone_number: str, message: str) -> bool:
        """
        Send SMS using Kavenegar API

        Args:
            phone_number: Recipient phone number (E.164 format)
            message: SMS content (max 70 chars)

        Returns:
            bool: True if sent successfully, False otherwise
        """
        if not settings.KAVENEGAR_API_KEY:
            logger.error("Kavenegar API key not configured")
            return False

        if not phone_number or not message:
            logger.error("Missing phone number or message")
            return False

        # Prepare request
        base_url = "https://api.kavenegar.com/v1"
        endpoint = f"{settings.KAVENEGAR_API_KEY}/sms/send.json"
        url = f"{base_url}/{endpoint}"

        payload = {
            "receptor": phone_number,
            "message": message,
            "sender": settings.KAVENEGAR_SENDER_NUMBER,
        }

        try:
            response = requests.post(url, data=payload, timeout=10)
            response.raise_for_status()
            json_response = response.json()

            # Check response status
            return_info = json_response.get("return", {})
            if return_info.get("status") == 200:
                logger.info(f"SMS sent to {phone_number}")
                return True

            # Handle error response
            error_msg = return_info.get('message', 'Unknown error')
            logger.error("Kavenegar API error: " f"{error_msg}")
            return False

        except requests.exceptions.RequestException as e:
            logger.exception(f"Kavenegar API request error: {str(e)}")
            return False

        except ValueError:
            logger.error("Invalid JSON response from Kavenegar")
            return False

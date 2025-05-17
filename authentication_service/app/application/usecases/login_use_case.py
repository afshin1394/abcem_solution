import uuid

import pyotp

from app.application.services.sms_service import SMSService
from app.application.services.token_service import TokenService
from app.application.usecases.base_use_case import BaseUseCase
from app.core.config import settings
from app.domain.cache.cache_gateway import CacheGateway
from app.domain.entities.otp_domain import LoginDomain


class LoginUseCase(BaseUseCase):
    def __init__(self, cache_gateway: CacheGateway, sms_service: SMSService, token_service: TokenService):
        self.cache_gateway = cache_gateway
        self.sms_service = sms_service
        self.token_service = token_service

    async def execute(self, msisdn: str) -> LoginDomain:
        # Generate a secure secret and session ID
        secret = pyotp.random_base32()
        session_id = str(uuid.uuid4())

        # Generate a TOTP code valid for 5 minutes (300 seconds)
        totp = pyotp.TOTP(secret, interval=int(settings.otp_expiration_time))
        otp_code = totp.now()

        # Store the secret tied to the phone number/session (with TTL)
        print("int(settings.otp_expiration_time)",int(settings.otp_expiration_time))
        print("int(settings.session_id_expiration_time)",int(settings.session_id_expiration_time))
        await self.cache_gateway.set(f"otp:otp_code:{session_id}", otp_code, int(settings.otp_expiration_time))
        await self.cache_gateway.set(f"msisdn:msisdn:{session_id}", msisdn, int(settings.session_id_expiration_time))

        # Send the OTP via SMS
        await self.sms_service.send_sms(msisdn, otp_code)

        # Return session ID (do not return OTP in production)
        return LoginDomain(session_id=session_id,otp= otp_code)

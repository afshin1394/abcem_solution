from app.application.repository.auth_repository import AuthRepository
from app.application.services.sms_service import SMSService
import random

from app.application.services.token_service import TokenService
from app.application.usecases.base_use_case import BaseUseCase
from app.domain.entities.otp_domain import LoginDomain
from app.domain.entities.user_domain import UserDomain


class LoginUseCase(BaseUseCase):
    def __init__(self, auth_repository: AuthRepository, sms_service: SMSService, token_service: TokenService):
        self.auth_repository = auth_repository
        self.sms_service = sms_service
        self.token_service = token_service

    async def execute(self, msisdn: str) -> LoginDomain:
        otp_code = str(random.randint(100000, 999999))
        session_id = await self.token_service.generate_session_id(UserDomain(msisdn=msisdn))
        login_domain = LoginDomain(session_id=session_id, otp=otp_code)
        await self.auth_repository.save_otp(otp=login_domain.otp)
        await self.auth_repository.save_session_id(session_id=session_id)
        await self.sms_service.send_sms(msisdn, otp_code)
        return LoginDomain(session_id=session_id, otp=otp_code)

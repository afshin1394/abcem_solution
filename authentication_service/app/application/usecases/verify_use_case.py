from app.application.usecases.base_use_case import BaseUseCase
from app.domain.entities.token_domain import TokenDomain
from app.application.repository.auth_repository import AuthRepository
from app.application.services.token_service import TokenService


class VerifyUseCase(BaseUseCase):
    def __init__(self, auth_repository: AuthRepository, token_service: TokenService):
        self.auth_repository = auth_repository
        self.token_service = token_service

    async def execute(self, session_id: str, otp_code: str) -> TokenDomain:
        stored_session_id = await self.auth_repository.get_session_id(session_id)
        otp = await self.auth_repository.get_otp(otp_code)

        if not stored_session_id or stored_session_id != session_id:
            raise ValueError("Invalid or expired session id")

        if not otp or otp != otp_code:
            raise ValueError("Invalid or expired OTP")
        tokens = await self.token_service.generate_tokens(session_id= stored_session_id,otp_code= otp_code)
        return tokens

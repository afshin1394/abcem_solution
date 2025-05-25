from app.application.usecases.base_use_case import BaseUseCase
from app.domain.cache.cache_gateway import CacheGateway
from app.domain.entities.token_domain import TokenDomain
from app.application.services.token_service import TokenService
from app.domain.exceptions import InvalidOTPException, InvalidSessionException, UserCreationException
from app.infrastructure.logto.services import find_user_by_phone_number, get_user_roles, create_user_and_assign_role


class VerifyUseCase(BaseUseCase):
    def __init__(self, cache_gateway : CacheGateway, token_service: TokenService):
        self.cache_gateway = cache_gateway
        self.token_service = token_service

    async def execute(self, session_id: str, otp: str) -> TokenDomain:
        print("session_id", session_id)
        msisdn = await self.cache_gateway.get(f"msisdn:msisdn:{session_id}")
        print("msisdn", msisdn)
        if not msisdn:
            raise InvalidOTPException()

        otp_code = await self.cache_gateway.get(f"otp:otp_code:{session_id}")
        print("otp_code", otp_code)
        if not otp_code or otp_code != otp:
            raise InvalidSessionException()

        user_id = await find_user_by_phone_number(msisdn=msisdn)
        if not user_id:
           success = await create_user_and_assign_role(username=f"user_{msisdn}",phone_number=msisdn,session_id=session_id,role_name="mobile_user")
           if not success:
               print("❌ User creation failed. Aborting token generation.")
               raise UserCreationException()

        print(f"user_id {user_id}")
        roles = []
        if user_id:
           roles = await get_user_roles(user_id=user_id)
           print(f"roles {roles} ")
        if not roles:
            roles.append("mobile_user")



        tokens = await self.token_service.generate_tokens(session_id= session_id,otp_code= otp_code,roles = roles)
        return tokens

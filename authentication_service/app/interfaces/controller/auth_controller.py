
from app.application.usecases.refresh_token_use_case import RefreshTokenUseCase
from app.application.usecases.login_use_case import LoginUseCase
from app.application.usecases.verify_use_case import VerifyUseCase
from app.interfaces.dto.request.login_request_dto import LoginRequestDto
from app.interfaces.dto.request.refresh_token_request_dto import RefreshTokenRequestDto
from app.interfaces.dto.request.verify_request_dto import VerifyRequestDTO
from app.interfaces.dto.response.login_response_dto import LoginResponseDTO
from app.interfaces.dto.response.refresh_token_response_dto import RefreshTokenResponseDTO
from app.interfaces.dto.response.verify_response_dto import VerifyResponseDTO


class AuthController:
    def __init__(self, verify_use_case: VerifyUseCase,
                 login_use_case: LoginUseCase,
                 refresh_token_use_case: RefreshTokenUseCase):
        self.verify_use_case = verify_use_case
        self.login_use_case = login_use_case
        self.refresh_token_use_case = refresh_token_use_case


    async def login(self, login_dto : LoginRequestDto)->LoginResponseDTO:
       return LoginResponseDTO.from_domain(otp_domain= await self.login_use_case.execute(msisdn=login_dto.msisdn))

    async def verify(self, verify_request_dto : VerifyRequestDTO)->VerifyResponseDTO:
       return VerifyResponseDTO.from_domain(token_domain= await self.verify_use_case.execute(session_id=verify_request_dto.session_id,otp_code=verify_request_dto.otp))

    async def refresh_token(self, refresh_token_request : RefreshTokenRequestDto)->RefreshTokenResponseDTO:
       return RefreshTokenResponseDTO.from_domain(access_token = await self.refresh_token_use_case.execute(refresh_token= refresh_token_request.refresh_token))
from app.application.usecases.logout_token_use_case import LogoutUseCase
from app.application.usecases.refresh_token_use_case import RefreshTokenUseCase
from app.application.usecases.login_use_case import LoginUseCase
from app.application.usecases.verify_use_case import VerifyUseCase
from app.interfaces.dto.request.login_request_dto import LoginRequestDto
from app.interfaces.dto.request.logout_request import LogoutRequest
from app.interfaces.dto.request.refresh_token_request_dto import RefreshTokenRequest
from app.interfaces.dto.request.verify_request_dto import VerifyRequestDTO
from app.interfaces.dto.response.login_response import LoginResponse
from app.interfaces.dto.response.logout_response import LogoutResponse
from app.interfaces.dto.response.refresh_token_response import RefreshTokenResponse
from app.interfaces.dto.response.verify_response import VerifyResponse


class AuthController:
    def __init__(self, verify_use_case: VerifyUseCase,
                 login_use_case: LoginUseCase,
                 refresh_token_use_case: RefreshTokenUseCase,
                 logout_use_case: LogoutUseCase,
                 ):

        self.verify_use_case = verify_use_case
        self.login_use_case = login_use_case
        self.refresh_token_use_case = refresh_token_use_case
        self.logout_use_case = logout_use_case


    async def login(self, login_dto : LoginRequestDto)->LoginResponse:
       return LoginResponse.from_domain(otp_domain= await self.login_use_case.execute(msisdn=login_dto.msisdn))

    async def verify(self, verify_request_dto : VerifyRequestDTO)->VerifyResponse:
        print("session_id",verify_request_dto.session_id)
        print("opt",verify_request_dto.otp)
        return VerifyResponse.from_domain(token_domain= await self.verify_use_case.execute(session_id=verify_request_dto.session_id, otp=verify_request_dto.otp))

    async def refresh_token(self, refresh_token_request : RefreshTokenRequest)->RefreshTokenResponse:
       token_domain = await self.refresh_token_use_case.execute(refresh_token=refresh_token_request.refresh_token)
       return RefreshTokenResponse.from_domain(access_token = token_domain.access_token, refresh_token=token_domain.refresh_token)


    async def logout(self,logout_request : LogoutRequest,access_token : str)->LogoutResponse:
       success = await self.logout_use_case.execute(refresh_token=logout_request.refresh_token,access_token =access_token)
       return LogoutResponse(status_code=200,result=success)
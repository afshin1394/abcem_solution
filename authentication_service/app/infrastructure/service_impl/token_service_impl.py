
import datetime
from app.application.services.token_service import TokenService
from app.domain.entities.user_domain import UserDomain
from app.domain.entities.token_domain import TokenDomain
SECRET_KEY = "your_secret_key"
from jose import jwt
class TokenServiceImpl(TokenService):
    async def generate_session_id(self, user: UserDomain) -> str:
        session_id = jwt.encode(
            {"msisdn": user.msisdn,"type": "session_id", "exp": datetime.datetime.now() + datetime.timedelta(minutes=2)},
            SECRET_KEY, algorithm="HS256")
        return session_id

    async def generate_tokens(self, session_id : str,otp_code : str) -> TokenDomain:
        access_token = jwt.encode(
            {"session_id": session_id, "otp" : otp_code ,"type": "access_token", "exp": datetime.datetime.now() + datetime.timedelta(minutes=15)},
            SECRET_KEY, algorithm="HS256")

        refresh_token = jwt.encode(
            {"session_id": session_id, "otp" : otp_code ,"type": "refresh_token", "exp": datetime.datetime.now() + datetime.timedelta(days=1)},
            SECRET_KEY, algorithm="HS256")

        return TokenDomain(access_token=access_token, refresh_token=refresh_token)

    async def refresh_access_token(self, refresh_token: str)-> str:
        decoded = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
        new_access_token = jwt.encode(
            {"msisdn": decoded['msisdn'],"type":"new_access_token", "exp": datetime.datetime.now() + datetime.timedelta(minutes=15)},
            SECRET_KEY, algorithm="HS256")

        return new_access_token
import datetime
from jose import jwt, JWTError
from app.application.services.token_service import TokenService
from app.core.config import settings
from app.domain.entities.user_domain import UserDomain
from app.domain.entities.token_domain import TokenDomain

# Load RSA Private & Public Keys
with open(settings.jwt_private_key, "r") as f:
    PRIVATE_KEY = f.read()
with open(settings.jwt_public_key, "r") as f:
    PUBLIC_KEY = f.read()

ALGORITHM = settings.jwt_encrypt_alg

class TokenServiceImpl(TokenService):



    async def validate_refresh_token(self, refresh_token: str) -> bool:
        try:
            decoded_token = jwt.decode(refresh_token, PUBLIC_KEY, algorithms=[ALGORITHM])

            if decoded_token["type"] != "refresh_token":
                raise ValueError("Invalid token type")

            # Manual expiration check
            exp = decoded_token.get("exp")
            if exp and datetime.datetime.utcfromtimestamp(exp) < datetime.datetime.utcnow():
                raise ValueError("Refresh token has expired")

            return True  # Token is valid

        except (JWTError, ValueError) as e:
            print(f"❌ Invalid or expired refresh token: {e}")
            return False

    async def generate_session_id(self, user: UserDomain) -> str:
        session_id = jwt.encode(
            {
                "sub": user.msisdn,
                "type": "session_id",
                "exp": datetime.datetime.now() + datetime.timedelta(minutes=2),
                "iss": settings.token_issuer_service,
            },
            PRIVATE_KEY, algorithm=ALGORITHM)
        return session_id

    async def generate_tokens(self, session_id: str, otp_code: str, **kwargs) -> TokenDomain:
        roles = kwargs.get("roles")
        scopes = kwargs.get("scopes", [])

        access_token = jwt.encode(
            {
                "sub": session_id,
                "otp": otp_code,
                "roles": roles,
                "scopes": scopes,
                "type": "access_token",
                "exp": datetime.datetime.now() + datetime.timedelta(minutes=15),
                "iss": settings.token_issuer_service,
                "aud": settings.audience
            },
            PRIVATE_KEY, algorithm=ALGORITHM)

        refresh_token = jwt.encode(
            {
                "sub": session_id,
                "otp": otp_code,
                "roles": roles,
                "scopes": scopes,
                "type": "refresh_token",
                "exp": datetime.datetime.now() + datetime.timedelta(days=30),
                "iss": settings.token_issuer_service,
            },
            PRIVATE_KEY, algorithm=ALGORITHM)

        return TokenDomain(access_token=access_token, refresh_token=refresh_token)

    async def generate_tokens_based_on_refresh_token(self, refresh_token: str) -> TokenDomain:
        decoded = jwt.decode(refresh_token, PUBLIC_KEY, algorithms=[ALGORITHM])


        access_token = jwt.encode(
            {
                "sub": decoded["sub"],
                "otp": decoded["otp"],
                "roles": decoded["roles"],
                "scopes": decoded["scopes"],
                "type": "access_token",
                "exp": datetime.datetime.now() + datetime.timedelta(minutes=15),
                "iss": settings.token_issuer_service,
                "aud": settings.audience
            },
            PRIVATE_KEY, algorithm=ALGORITHM)

        refresh_token = jwt.encode(
            {
                "sub": decoded["sub"],
                "otp": decoded["otp"],
                "roles": decoded["roles"],
                "scopes": decoded["scopes"],
                "type": "refresh_token",
                "exp": datetime.datetime.now() + datetime.timedelta(days=30),
                "iss": settings.token_issuer_service,
            },
            PRIVATE_KEY, algorithm=ALGORITHM)

        return TokenDomain(access_token=access_token, refresh_token=refresh_token)




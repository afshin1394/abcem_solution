import datetime

from jose import jwt, JWTError
from app.core.config import settings


from app.domain.services.token_service import TokenService

# Load RSA Private & Public Keys
with open(settings.jwt_private_key, "r") as f:
    PRIVATE_KEY = f.read()
with open(settings.jwt_public_key, "r") as f:
    PUBLIC_KEY = f.read()

ALGORITHM = settings.jwt_encrypt_alg


class TokenServiceImpl(TokenService):

    async def validate_access_token(self, access_token: str) -> bool:
        try:
            decoded_token = jwt.decode(access_token, PUBLIC_KEY, algorithms=[ALGORITHM])

            if decoded_token["type"] != "access_token":
                raise ValueError("Invalid token type")

            # Manual expiration check
            exp = decoded_token.get("exp")
            if exp and datetime.datetime.utcfromtimestamp(exp) < datetime.datetime.utcnow():
                return False

            return True  # Token is valid

        except (JWTError, ValueError) as e:
            return False


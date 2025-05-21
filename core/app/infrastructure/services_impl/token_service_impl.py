import datetime

from jose import jwt, JWTError, ExpiredSignatureError
from jose.exceptions import JWTClaimsError

from app.core.config import settings
from app.domain.exceptions import AccessTokenInvalidException, AccessTokenTypeInvalidException, \
    AccessTokenExpiredException

from app.domain.services.token_service import TokenService

# Load RSA Private & Public Keys
with open(settings.jwt_private_key, "r") as f:
    PRIVATE_KEY = f.read()
with open(settings.jwt_public_key, "r") as f:
    PUBLIC_KEY = f.read()

ALGORITHM = settings.jwt_encrypt_alg


class TokenServiceImpl(TokenService):

    async def validate_access_token(self, access_token: str) -> dict:
        try:
            decoded_token = jwt.decode(
                access_token,
                PUBLIC_KEY,
                algorithms=[ALGORITHM],
                audience=settings.expecting_aud,
                issuer=settings.jwt_issuer,
            )

            # Validate required claims
            required_claims = ["sub", "exp", "type"]
            for claim in required_claims:
                if claim not in decoded_token:
                    raise AccessTokenInvalidException(f"Missing claim: {claim}")

            # Check token type
            if decoded_token["type"] != "access_token":
                raise AccessTokenTypeInvalidException()

            # Optional: Check `nbf` if included
            nbf = decoded_token.get("nbf")
            if nbf and datetime.datetime.utcnow().timestamp() < nbf:
                raise AccessTokenInvalidException("Token not yet valid (nbf)")

            return decoded_token  # Return the claims if valid

        except ExpiredSignatureError:
            raise AccessTokenExpiredException()

        except JWTClaimsError as e:
            raise AccessTokenInvalidException(f"Invalid claims: {str(e)}")

        except JWTError as e:
            raise AccessTokenInvalidException(f"JWT error: {str(e)}")

        except Exception as e:
            raise AccessTokenInvalidException(f"Unknown error: {str(e)}")

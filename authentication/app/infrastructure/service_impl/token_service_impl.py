import datetime

from jose import jwt, JWTError, ExpiredSignatureError
from jose.exceptions import JWTClaimsError

from app.application.services.token_service import TokenService
from app.core.config import settings
from app.domain.entities.user_domain import UserDomain
from app.domain.entities.token_domain import TokenDomain
from app.domain.exceptions import AccessTokenTypeInvalidException, AccessTokenExpiredException, \
    AccessTokenInvalidException

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
                audience=settings.expected_aud,
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
        exp_access_token = datetime.datetime.now() + datetime.timedelta(minutes=15)
        access_token = jwt.encode(
            {
                "sub": session_id,
                "otp": otp_code,
                "roles": roles,
                "scopes": scopes,
                "type": "access_token",
                "exp": exp_access_token,
                "iss": settings.token_issuer_service,
                "aud": settings.audience_list
            },
            PRIVATE_KEY, algorithm=ALGORITHM)
        access_token_expiration_date = exp_access_token.isoformat()

        exp_refresh_token = datetime.datetime.now() + datetime.timedelta(days=30)
        refresh_token = jwt.encode(
            {
                "sub": session_id,
                "otp": otp_code,
                "roles": roles,
                "scopes": scopes,
                "type": "refresh_token",
                "exp": exp_refresh_token,
                "iss": settings.token_issuer_service,
            },
            PRIVATE_KEY, algorithm=ALGORITHM)
        refresh_token_expiration_date = exp_refresh_token.isoformat()
        return TokenDomain(access_token=access_token,access_token_expiration_date= access_token_expiration_date, refresh_token=refresh_token,refresh_token_expiration_date= refresh_token_expiration_date)

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
                "aud": settings.audience_list
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

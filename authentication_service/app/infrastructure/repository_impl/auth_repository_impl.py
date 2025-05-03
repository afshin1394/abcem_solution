from app.application.repository.auth_repository import AuthRepository
from app.infrastructure.redis import RedisClient


class AuthRepositoryImpl(AuthRepository):

    def __init__(self, redis_client: RedisClient):
        self.redis_client = redis_client

    async def save_otp(self, otp: str):
        await self.redis_client.set(otp, otp, expire=300)

    async def get_otp(self, otp: str) -> str:
        otp_code = await self.redis_client.redis.get(otp)
        return otp_code


    async def save_session_id(self, session_id: str):
       print(f"session_id:\n {session_id}")
       await self.redis_client.set(session_id, session_id, expire=300)


    async def get_session_id(self, session_id: str) -> str:
        session_id = await self.redis_client.redis.get(session_id)
        return session_id if session_id else None

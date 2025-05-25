from app.infrastructure.service_impl.token_service_impl import TokenServiceImpl


async def get_token_service():
    return TokenServiceImpl()
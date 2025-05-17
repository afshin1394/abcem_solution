from fastapi import Depends

from app.application.services.sms_service import SMSService
from app.application.services.token_service import TokenService
from app.application.usecases.login_use_case import LoginUseCase
from app.domain.cache.cache_gateway import CacheGateway
from app.infrastructure.di.redis_client import get_cache
from app.infrastructure.di.services.sms_service import get_sms_service
from app.infrastructure.di.services.token_service import get_token_service


async def get_login_use_case(cache_gateway: CacheGateway = Depends(get_cache),sms_service: SMSService = Depends(get_sms_service), token_service: TokenService = Depends(get_token_service)):
    return LoginUseCase(cache_gateway=cache_gateway, sms_service= sms_service,token_service=token_service)
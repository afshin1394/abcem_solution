from app.infrastructure.service_impl.sms_service_impl import SMSServiceImpl


async def get_sms_service():
    return SMSServiceImpl()
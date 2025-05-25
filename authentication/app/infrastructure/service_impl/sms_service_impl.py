from app.application.services.sms_service import SMSService
from app.infrastructure.exceptions import SMSServicesException


class SMSServiceImpl(SMSService):
    async def send_sms(self, msisdn: str, otp: str):
        try:
           print(f'otp {otp} sent to {msisdn} ...')
           # api = KavenegarAPI(
           #         '616F6A3473416D76463474446B366D6E4D5A7236595958464D315237343658456638324F744238696E6D633D')
           # params = {
           #         'receptor': msisdn,
           #         'template': 'verificationcode',
           #         'token': otp,
           #         'type': 'sms',  # sms vs call
           # }
           # response = api.verify_lookup(params)
           # print(response)

        except Exception as ex:
            print("exception happened",ex)
            raise SMSServicesException








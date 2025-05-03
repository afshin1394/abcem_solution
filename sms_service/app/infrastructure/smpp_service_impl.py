import logging
import sys
import smpplib.gsm
import smpplib.client
import smpplib.consts


from app.domain.smpp_service import SmppService

# Configure logging
logging.basicConfig(level=logging.DEBUG)


class SMPPServiceImpl(SmppService):

    def __init__(self, host: str, port: int, system_id: str, password: str):
        self.host = host
        self.port = port
        self.system_id = system_id
        self.password = password
        self.client = smpplib.client.Client(self.host, self.port, allow_unknown_opt_params=True)

        # Handlers
        self.client.set_message_sent_handler(
            lambda pdu: sys.stdout.write(f"Sent {pdu.sequence} {pdu.message_id}\n"))
        self.client.set_message_received_handler(
            lambda pdu: sys.stdout.write(f"Delivered {pdu.receipted_message_id}\n"))

        # Connect and bind
        self.client.connect()
        self.client.bind_transceiver(system_id=self.system_id, password=self.password)

    async def send_sms(self, phone: str, message: str):
        parts, encoding_flag, msg_type_flag = smpplib.gsm.make_parts(message)

        sms_ids = []
        for part in parts:
            pdu = self.client.send_message(
                source_addr_ton=smpplib.consts.SMPP_TON_INTL,
                source_addr="SENDERPHONENUM",
                dest_addr_ton=smpplib.consts.SMPP_TON_INTL,
                destination_addr=phone,
                short_message=part,
                data_coding=encoding_flag,
                esm_class=msg_type_flag,
                registered_delivery=True,
            )
            sms_ids.append(pdu.sequence)
            print(f"SMS {pdu.sequence} sent to {phone}")

        return sms_ids

    async def listen(self):
        """Start listening for incoming delivery receipts."""
        self.client.listen()
import socket
import uuid
from pythonjsonlogger import jsonlogger

from app.core.config import settings


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)

        # Add default fields
        log_record['service_name'] = settings.app_name
        log_record['environment'] = settings.app_env
        log_record['hostname'] = socket.gethostname()

        # Add a dummy correlation ID if not provided (optional)
        if 'correlation_id' not in log_record:
            log_record['correlation_id'] = str(uuid.uuid4())




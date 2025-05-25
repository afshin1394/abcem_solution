# --- Now the tests ---
import pytest
from pydantic import ValidationError

from app.interfaces.dto.request.send_sms_request import SendSmsRequest


@pytest.mark.parametrize("valid_number", [
    "09121234560",  # MCI
    "+989351234567",  # Irancell
    "+989011234567",  # Irancell TDD
    "+989021234567",  # Irancell TDD Modem
    "+989041234567",  # Irancell TDD Modem
    "+989911234567",  # MCI New range
])
def test_valid_phone_numbers(valid_number):
    """Test that valid Iranian numbers pass."""
    request = SendSmsRequest(phone_number=valid_number, message="Test message")
    assert request.phone_number == valid_number


@pytest.mark.parametrize("invalid_number", [
    "09121234567",        # Missing '+'
    "+98912123456",        # Too short
    "+9891212345678",      # Too long
    "+979121234567",       # Wrong country code
    "+989001234567",       # Invalid prefix (900 not allowed)
    "+989421234567",       # Invalid prefix (942 not allowed)
    "+98912abc4567",       # Letters inside number
    "+98912123 4567",      # Space inside number
])
def test_invalid_phone_numbers(invalid_number):
    """Test that invalid Iranian numbers raise ValidationError."""
    with pytest.raises(ValidationError):
        SendSmsRequest(phone_number=invalid_number, message="Test message")
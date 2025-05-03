from app.application.feature.shared.command import Command


class InsertSmsCommand(Command):
    phone_number: str
    message: str

    def __repr__(self):
        message_preview = (self.message[:20] + '...') if len(self.message) > 20 else self.message
        return (
            f"InsertSmsCommand(phone_number={self.phone_number!r}, "
            f"message={message_preview!r})"
        )
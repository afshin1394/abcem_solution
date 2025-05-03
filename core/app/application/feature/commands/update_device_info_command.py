from datetime import datetime

from app.application.feature.shared.command import Command


class UpdateDeviceInfoCommand(Command):
    walk_test_id: str
    security_patch: datetime
    sdk: int
    os_version: int
    brand: str
    device: str
    hardware: str
    model: str
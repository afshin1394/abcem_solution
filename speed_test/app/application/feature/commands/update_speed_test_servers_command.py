from app.application.feature.shared.command import Command
from app.domain.entities.speed_test_server_domain import SpeedTestServerDomain


class UpdateSpeedTestServersCommand(Command):
      servers : list[SpeedTestServerDomain]

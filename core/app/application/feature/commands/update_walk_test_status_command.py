from app.application.feature.shared.command import Command
from app.domain.enums.walk_test_state_enum import WalkTestStatusEnum


class UpdateWalkTestStatusCommand(Command):
      walk_test_id : str
      walk_test_status : WalkTestStatusEnum
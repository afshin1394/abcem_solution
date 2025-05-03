from pydantic import BaseModel

from app.domain.enums.walk_test_state_enum import WalkTestStatusEnum


class UpdateWalkTestStatusRequest(BaseModel):
      walk_test_id : str
      walk_test_status : WalkTestStatusEnum
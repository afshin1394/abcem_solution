from pydantic import BaseModel


class WalkTestResultsByWalkTestIdRequest(BaseModel):
       walk_test_id: str
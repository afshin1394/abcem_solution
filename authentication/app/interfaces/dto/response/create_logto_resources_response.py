from typing import Optional

from pydantic import BaseModel

from app.interfaces.dto.success_response import BaseSuccessResponse


class Scope(BaseModel):
    tenantId: str
    id: str
    resourceId: str
    name: str
    description: str
    createdAt: int


class LogtoResource(BaseModel):
    tenantId: str
    id: str
    name: str
    indicator: str
    isDefault: bool
    accessTokenTtl: int
    scopes: Optional[list[Scope]]

class LogtoResourcesSuccessResponse(BaseSuccessResponse[LogtoResource]):
      pass

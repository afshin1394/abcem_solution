from fastapi import APIRouter, Depends

from app.infrastructure.di.controllers import get_technology_type_controller
from app.interfaces.controllers.technology_type_controller import TechnologyTypeController
from app.interfaces.dto.response.technology_type_response import TechnologyTypeResponse

router_v1 = APIRouter(
    prefix="/technology_type",
    tags=["technology_type"]
)


@router_v1.get("/get_all", response_model=TechnologyTypeResponse)
async def get_all(technology_controller: TechnologyTypeController = Depends(get_technology_type_controller)) -> TechnologyTypeResponse:
    return await technology_controller.get_all()

from fastapi import APIRouter, Depends

from app.infrastructure.di.controllers import get_all_problematic_service_type_controller
from app.interfaces.controllers.problematic_service_type_controller import ProblematicServiceTypeController
from app.interfaces.dto.response.problematic_service_response import  ProblematicServiceResponse

router_v1 = APIRouter(
    prefix="/problematic_service_type",
    tags=["problematic_service"],
)


@router_v1.get("/get_all", response_model = ProblematicServiceResponse)
async def get_all(problematic_service_type_controller : ProblematicServiceTypeController = Depends(get_all_problematic_service_type_controller)) :
    return await problematic_service_type_controller.get_all()
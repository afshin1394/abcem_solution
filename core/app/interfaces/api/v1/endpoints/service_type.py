from fastapi import APIRouter, Depends

from app.infrastructure.di.controllers import get_all_service_type_controller
from app.interfaces.controllers.service_type_controller import ServiceTypeController
from app.interfaces.dto.response.service_type_response import ServiceTypeResponse

router_v1 = APIRouter(
    prefix="/service_type",
    tags=["service_type"],
)


@router_v1.get("/get_all", response_model = ServiceTypeResponse)
async def get_all(service_type_controller : ServiceTypeController = Depends(get_all_service_type_controller)) :
    return await service_type_controller.get_all()
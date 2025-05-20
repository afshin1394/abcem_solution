from fastapi import APIRouter, Depends

from app.infrastructure.di.controllers import get_all_service_type_controller
from app.infrastructure.di.usecases import get_validate_token_use_case
from app.interfaces.controllers.service_type_controller import ServiceTypeController
from app.interfaces.dto.response.service_type_response import ServiceTypeResponse


router_public = APIRouter(prefix="/public/config/service_type")
router_protected = APIRouter(prefix="/protected/config/service_type",dependencies=[Depends(get_validate_token_use_case)])
router_private = APIRouter(prefix="/private/config/service_type")

@router_protected.get("/get_all", response_model = ServiceTypeResponse)
async def get_all(service_type_controller : ServiceTypeController = Depends(get_all_service_type_controller)) :
    return await service_type_controller.get_all()
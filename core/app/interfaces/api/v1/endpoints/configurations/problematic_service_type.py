from fastapi import APIRouter, Depends

from app.infrastructure.di.controllers import get_all_problematic_service_type_controller
from app.infrastructure.di.usecases import get_validate_token_use_case
from app.interfaces.controllers.problematic_service_type_controller import ProblematicServiceTypeController
from app.interfaces.dto.response.problematic_service_response import  ProblematicServiceResponse


router_public = APIRouter(prefix="/public/config/problematic_service_type")
router_protected = APIRouter(prefix="/protected/problematic_service_type",dependencies=[Depends(get_validate_token_use_case)])
router_private = APIRouter(prefix="/private/problematic_service_type")

@router_protected.get("/get_all", response_model = ProblematicServiceResponse)
async def get_all(problematic_service_type_controller : ProblematicServiceTypeController = Depends(get_all_problematic_service_type_controller)) :
    return await problematic_service_type_controller.get_all()
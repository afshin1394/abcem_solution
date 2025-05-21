from fastapi import APIRouter, Depends

from app.infrastructure.di.api_key_header import get_validate_token
from app.infrastructure.di.controllers import get_technology_type_controller
from app.infrastructure.di.usecases import get_validate_token_use_case
from app.interfaces.controllers.technology_type_controller import TechnologyTypeController
from app.interfaces.dto.response.technology_type_response import TechnologyTypeResponse


router_public = APIRouter(prefix="/public/config/technology_type")
router_protected = APIRouter(prefix="/protected/config/technology_type",dependencies=[Depends(get_validate_token)])
router_private = APIRouter(prefix="/private/config/technology_type")

@router_protected.get("/get_all", response_model=TechnologyTypeResponse)
async def get_all(technology_controller: TechnologyTypeController = Depends(get_technology_type_controller)) -> TechnologyTypeResponse:
    return await technology_controller.get_all()

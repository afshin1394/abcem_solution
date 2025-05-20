from fastapi import APIRouter, Depends

from app.infrastructure.di.controllers import get_all_complaint_type_controller
from app.infrastructure.di.usecases import get_validate_token_use_case
from app.interfaces.controllers.complaint_type_controller import ComplaintTypeController
from app.interfaces.dto.response.complaint_type_response import ComplaintTypeResponse

router_public = APIRouter(prefix="/public/config/complaint_type")
router_protected = APIRouter(prefix="/protected/config/complaint_type",dependencies=[Depends(get_validate_token_use_case)])
router_private = APIRouter(prefix="/private/config/complaint_type")

@router_protected.get("/get_all", response_model = ComplaintTypeResponse)
async def get_all(complaint_type_controller : ComplaintTypeController = Depends(get_all_complaint_type_controller)) :
    return await complaint_type_controller.get_all()


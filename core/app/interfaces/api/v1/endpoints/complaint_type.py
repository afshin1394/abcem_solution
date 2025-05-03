from fastapi import APIRouter, Depends

from app.infrastructure.di.controllers import get_all_complaint_type_controller
from app.interfaces.controllers.complaint_type_controller import ComplaintTypeController
from app.interfaces.dto.response.complaint_type_response import ComplaintTypeResponse

router_v1 = APIRouter(
    prefix="/complaint_type",
    tags=["complaint_type"],
)
@router_v1.get("/get_all", response_model = ComplaintTypeResponse)
async def get_all(complaint_type_controller : ComplaintTypeController = Depends(get_all_complaint_type_controller)) :
    return await complaint_type_controller.get_all()
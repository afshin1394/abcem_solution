from fastapi import APIRouter, Depends

from app.infrastructure.di.controllers import get_all_test_step_type_controller
from app.infrastructure.di.usecases import get_validate_token_use_case
from app.interfaces.controllers.test_step_type_controller import TestStepTypeController
from app.interfaces.dto.response.test_step_type_response import TestStepTypeResponse


router_public = APIRouter(prefix="/public/config/test_step_type")
router_protected = APIRouter(prefix="/protected/config/test_step_type",dependencies=[Depends(get_validate_token_use_case)])
router_private = APIRouter(prefix="/private/config/test_step_type")

@router_protected.get("/get_all", response_model=TestStepTypeResponse)
async def get_all(test_step_type_controller: TestStepTypeController = Depends(get_all_test_step_type_controller)) -> TestStepTypeResponse:
    return await test_step_type_controller.get_all()

from fastapi import APIRouter, Depends

from app.infrastructure.di.controllers import get_all_test_step_type_controller
from app.interfaces.controllers.test_step_type_controller import TestStepTypeController
from app.interfaces.dto.response.test_step_type_response import TestStepTypeResponse

router_v1 = APIRouter(
    prefix="/test_step_type",
    tags=["test_step_type"]
)


@router_v1.get("/get_all", response_model=TestStepTypeResponse)
async def get_all(test_step_type_controller: TestStepTypeController = Depends(get_all_test_step_type_controller)) -> TestStepTypeResponse:
    return await test_step_type_controller.get_all()

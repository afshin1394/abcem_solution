from app.application.usecase.get_all_test_step_type_usecase import GetAllTestStepTypeUseCase
from app.infrastructure.mapper.mapper import map_models_list
from app.interfaces.dto.response.test_step_type_response import TestStepTypeResponse, TestStepType


class TestStepTypeController:


    def __init__(self, get_all_test_step_type_use_case : GetAllTestStepTypeUseCase):
        self.get_all_test_step_type_use_case = get_all_test_step_type_use_case


    async def get_all(self) -> TestStepTypeResponse:
       test_step_type_domain_list = await self.get_all_test_step_type_use_case()
       test_step_type_list = await map_models_list(test_step_type_domain_list, TestStepType)
       return TestStepTypeResponse(result=test_step_type_list)
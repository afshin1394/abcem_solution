from app.application.usecase.get_all_problematic_service_types_usecase import GetAllProblematicServiceTypesUseCase
from app.infrastructure.mapper.mapper import map_models_list
from app.interfaces.dto.response.problematic_service_response import ProblematicServiceResponse, ProblematicService


class ProblematicServiceTypeController:
    def __init__(self,get_all_problematic_service_types_use_case : GetAllProblematicServiceTypesUseCase):
        self.get_all_problematic_service_types_use_case = get_all_problematic_service_types_use_case

    async def get_all(self) -> ProblematicServiceResponse:
        problematic_service_domain_list = await self.get_all_problematic_service_types_use_case()
        problematic_service_response_list = await map_models_list(problematic_service_domain_list, ProblematicService)
        return ProblematicServiceResponse(result=problematic_service_response_list)
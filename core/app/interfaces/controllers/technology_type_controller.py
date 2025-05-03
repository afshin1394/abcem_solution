from app.application.usecase.get_all_technology_type_usecase import GetAllTechnologyTypesUseCase
from app.infrastructure.mapper.mapper import map_models_list
from app.interfaces.dto.response.technology_type_response import TechnologyTypeResponse, TechnologyType


class TechnologyTypeController:
    def __init__(self, get_all_technology_types_use_case: GetAllTechnologyTypesUseCase) -> None:
        self.get_all_technology_types_use_case = get_all_technology_types_use_case

    async def get_all(self) -> TechnologyTypeResponse:
        technology_type_domain_list = await self.get_all_technology_types_use_case()
        technology_type_list = await map_models_list(technology_type_domain_list, TechnologyType)
        return TechnologyTypeResponse(result=technology_type_list)

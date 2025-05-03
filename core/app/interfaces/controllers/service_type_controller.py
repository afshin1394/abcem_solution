from app.application.usecase.get_all_service_type_usecase import GetAllServiceTypeUseCase
from app.infrastructure.mapper.mapper import map_models_list
from app.interfaces.dto.response.service_type_response import ServiceTypeResponse, ServiceType


class ServiceTypeController:

    def __init__(self, get_all_service_type_use_case: GetAllServiceTypeUseCase):
        self.get_all_service_type_use_case = get_all_service_type_use_case


    async def get_all(self) -> ServiceTypeResponse:
        service_type_domain_list = await self.get_all_service_type_use_case()
        service_type_response_list = await map_models_list(service_type_domain_list, ServiceType)
        return ServiceTypeResponse(result=service_type_response_list)

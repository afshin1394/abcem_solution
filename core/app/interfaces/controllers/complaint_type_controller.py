from app.application.usecase.get_all_complaint_types_usecase import GetAllComplaintTypesUseCase
from app.infrastructure.mapper.mapper import map_models_list
from app.interfaces.dto.response.complaint_type_response import ComplaintTypeResponse, ComplaintType


class ComplaintTypeController:

    def __init__(self,get_all_complaint_type_use_case : GetAllComplaintTypesUseCase):
        self.get_all_complaint_type_use_case = get_all_complaint_type_use_case

    async def get_all(self) -> ComplaintTypeResponse:
       complaint_domain_list = await self.get_all_complaint_type_use_case()
       complaint_response_list = await map_models_list(complaint_domain_list,ComplaintType)
       return ComplaintTypeResponse(result=complaint_response_list)
from app.application.usecase.get_all_speed_test_servers_usecase import GetAllSpeedTestServersUseCase
from app.application.usecase.update_speed_test_server_use_case import UpdateSpeedTestServersUseCase
from app.infrastructure.mapper.mapper import map_models_list
from app.interfaces.dto.request.update_speed_test_servers_request import UpdateSpeedTestServersRequest
from app.interfaces.dto.response.speed_test_server_response import SpeedTestsServersResponse, SpeedTestServer


class SpeedTestServerController:

    def __init__(self, update_speed_test_server_use_case: UpdateSpeedTestServersUseCase,get_all_speed_test_servers_use_case : GetAllSpeedTestServersUseCase) -> None:
        self.update_speed_test_server_use_case = update_speed_test_server_use_case
        self.get_all_speed_test_servers_use_case = get_all_speed_test_servers_use_case

    async def update_speed_test_servers(self,update_speed_test_server_request: UpdateSpeedTestServersRequest) -> None:

         await self.update_speed_test_server_use_case(update_speed_test_server_request = update_speed_test_server_request)
         return SpeedTestsServersResponse(status_code = 204,result= None)


    async def get_all_speed_test_servers(self) -> None:
        servers_domain_list = await self.get_all_speed_test_servers_use_case()
        print(f"servers_domain_list -------------->>>>>>>>>>>>>>>>> {servers_domain_list}")
        servers_response_list = await map_models_list(servers_domain_list,SpeedTestServer)
        print(f"servers_response_list -------------->>>>>>>>>>>>>>>>> {servers_response_list}")

        return SpeedTestsServersResponse(result=servers_response_list)
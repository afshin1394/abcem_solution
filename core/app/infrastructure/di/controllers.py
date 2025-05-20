from fastapi import Depends

from app.application.usecase.create_user_usecase import CreateUserUseCase
from app.application.usecase.create_walk_test_usecase import CreateWalkTestUseCase
from app.application.usecase.get_all_complaint_types_usecase import GetAllComplaintTypesUseCase
from app.application.usecase.get_all_problematic_service_types_usecase import GetAllProblematicServiceTypesUseCase
from app.application.usecase.get_all_service_type_usecase import GetAllServiceTypeUseCase
from app.application.usecase.get_all_speed_test_servers_usecase import GetAllSpeedTestServersUseCase
from app.application.usecase.get_all_technology_type_usecase import GetAllTechnologyTypesUseCase
from app.application.usecase.get_all_test_step_type_usecase import GetAllTestStepTypeUseCase
from app.application.usecase.get_all_walk_test_by_msisdn_usecase import GetAllWalkTestByMSISDNUseCase
from app.application.usecase.get_walk_test_results_by_walk_test_id_use_case import GetWalkTestResultsByWalkTestIdUseCase
from app.application.usecase.insert_walk_test_results_use_case import InsertWalkTestResultsUseCase
from app.application.usecase.speed_test_server_list_usecase import SpeedTestServerListUseCase
from app.application.usecase.update_device_info_usecase import UpdateDeviceInfoUseCase
from app.application.usecase.update_speed_test_server_use_case import UpdateSpeedTestServersUseCase
from app.application.usecase.update_walk_test_status_use_case import UpdateWalkTestStatusUseCase
from app.application.usecase.validate_walk_test_process_usecase import ValidateWalkTestProcessUseCase
from app.infrastructure.di.usecases import get_create_user_use_case, get_speed_test_use_case, \
    get_create_walk_test_use_case, get_all_walk_test_by_msisdn_use_case, get_all_technology_type_use_case, \
    get_all_complaint_type_use_case, get_all_problematic_service_type_use_case, get_all_service_type_use_case, \
    get_all_test_step_type_use_case, get_update_device_info_use_case, get_insert_walk_test_results_use_case, \
    get_walk_test_results_by_walk_test_id_use_case, get_update_walk_test_status_use_case, \
    get_update_speed_test_servers_use_case, get_all_speed_test_servers_use_case, get_validate_walk_test_process_use_case
from app.interfaces.controllers.complaint_type_controller import ComplaintTypeController
from app.interfaces.controllers.device_info_controller import DeviceInfoController
from app.interfaces.controllers.problematic_service_type_controller import ProblematicServiceTypeController
from app.interfaces.controllers.service_type_controller import ServiceTypeController
from app.interfaces.controllers.speed_test_controller import SpeedTestServerController
from app.interfaces.controllers.technology_type_controller import TechnologyTypeController
from app.interfaces.controllers.test_step_type_controller import TestStepTypeController
from app.interfaces.controllers.user_controller import UserController
from app.interfaces.controllers.walk_test_controller import WalkTestController
from app.interfaces.controllers.walk_test_results_controller import WalkTestResultsController


async def get_create_user_controller(create_user_use_case: CreateUserUseCase = Depends(get_create_user_use_case),
                                     speed_test_server_list_use_case: SpeedTestServerListUseCase = Depends(
                                         get_speed_test_use_case)) -> UserController:
    return UserController(create_user_use_case=create_user_use_case,
                          speed_test_server_list_use_case=speed_test_server_list_use_case)


async def get_walk_test_controller(
        create_walk_test_use_case: CreateWalkTestUseCase = Depends(get_create_walk_test_use_case),
        get_walk_test_by_msisdn_use_case: GetAllWalkTestByMSISDNUseCase =
        Depends(get_all_walk_test_by_msisdn_use_case),
        __update_walk_test_status_use_case : UpdateWalkTestStatusUseCase = Depends(get_update_walk_test_status_use_case),
        validate_walk_test_process_use_case : ValidateWalkTestProcessUseCase = Depends(get_validate_walk_test_process_use_case)
) -> WalkTestController:
    return WalkTestController(
        create_walk_test_use_case=create_walk_test_use_case,
        get_all_walk_test_by_msisdn_use_case=get_walk_test_by_msisdn_use_case,
        update_walk_test_status_use_case=__update_walk_test_status_use_case,
        validate_walk_test_process_use_case=validate_walk_test_process_use_case,
    )

async def get_walk_test_results_controller(
        insert_walk_test_results_use_case: InsertWalkTestResultsUseCase = Depends(get_insert_walk_test_results_use_case),
        walk_test_results_by_walk_test_id_use_case : GetWalkTestResultsByWalkTestIdUseCase = Depends(get_walk_test_results_by_walk_test_id_use_case),
) -> WalkTestResultsController:
    return WalkTestResultsController(
        insert_walk_test_results_use_case=insert_walk_test_results_use_case,
        get_walk_test_results_by_walk_test_id_use_case=walk_test_results_by_walk_test_id_use_case,
    )


async def get_device_info_controller(
        update_device_info_use_case: UpdateDeviceInfoUseCase = Depends(get_update_device_info_use_case),
) -> DeviceInfoController:
    return DeviceInfoController(
        update_device_info_use_case=update_device_info_use_case,
    )


async def get_technology_type_controller(technology_type_use_case: GetAllTechnologyTypesUseCase = Depends(
    get_all_technology_type_use_case)) -> TechnologyTypeController:
    return TechnologyTypeController(
        get_all_technology_types_use_case=technology_type_use_case
    )


async def get_all_complaint_type_controller(complaint_type_use_case: GetAllComplaintTypesUseCase = Depends(
    get_all_complaint_type_use_case)) -> ComplaintTypeController:
    return ComplaintTypeController(
        get_all_complaint_type_use_case=complaint_type_use_case
    )


async def get_all_problematic_service_type_controller(
        problematic_service_type_use_case: GetAllProblematicServiceTypesUseCase = Depends(
            get_all_problematic_service_type_use_case)) -> ProblematicServiceTypeController:
    return ProblematicServiceTypeController(
        get_all_problematic_service_types_use_case=problematic_service_type_use_case
    )


async def get_all_service_type_controller(service_type_use_case: GetAllServiceTypeUseCase = Depends(
    get_all_service_type_use_case)) -> ServiceTypeController:
    return ServiceTypeController(
        get_all_service_type_use_case=service_type_use_case
    )


async def get_all_test_step_type_controller(test_step_type_use_case: GetAllTestStepTypeUseCase = Depends(
    get_all_test_step_type_use_case)) -> TestStepTypeController:
    return TestStepTypeController(
        get_all_test_step_type_use_case=test_step_type_use_case,
    )


async def get_update_device_info_controller(update_device_info_use_case: UpdateDeviceInfoUseCase = Depends(
    get_update_device_info_use_case)) -> DeviceInfoController:
    return DeviceInfoController(
        update_device_info_use_case=update_device_info_use_case
    )
async def get_speed_test_servers_controller(update_speed_test_server_use_case: UpdateSpeedTestServersUseCase = Depends(get_update_speed_test_servers_use_case),all_speed_test_servers_use_case : GetAllSpeedTestServersUseCase = Depends(get_all_speed_test_servers_use_case)) -> SpeedTestServerController:
    return SpeedTestServerController(
        update_speed_test_server_use_case = update_speed_test_server_use_case,
        get_all_speed_test_servers_use_case=all_speed_test_servers_use_case,
    )

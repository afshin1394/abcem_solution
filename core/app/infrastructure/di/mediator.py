from fastapi import Depends

from app.application.feature.commands.authenticate_command import AuthenticateCommand
from app.application.feature.commands.create_user_command import CreateUserCommand
from app.application.feature.commands.create_walk_test_command import CreateWalkTestCommand
from app.application.feature.commands.create_walk_test_results_command import CreateWalkTestResultsCommand
from app.application.feature.commands.update_device_info_command import UpdateDeviceInfoCommand
from app.application.feature.commands.update_entered_at_walk_test_command import UpdateEnteredAtWalkTestCommand
from app.application.feature.commands.update_speed_test_servers_command import UpdateSpeedTestServersCommand
from app.application.feature.commands.update_walk_test_status_command import UpdateWalkTestStatusCommand
from app.application.feature.handlers.command_handler.authenticate_command_handler import AuthenticateCommandHandler
from app.application.feature.handlers.command_handler.create_user_command_handler import CreateUserCommandHandler
from app.application.feature.handlers.command_handler.create_walk_test_command_handler import CreateWalkTestCommandHandler
from app.application.feature.handlers.command_handler.create_walk_test_results_command_handler import \
    CreateWalkTestResultsCommandHandler
from app.application.feature.handlers.command_handler.update_device_info_command_handler import \
    UpdateDeviceInfoCommandHandler
from app.application.feature.handlers.command_handler.update_entered_command_handler import UpdateEnteredAtWalkTestCommandHandler
from app.application.feature.handlers.command_handler.update_speed_test_servers_command_handler import \
    UpdateSpeedTestServersCommandHandler
from app.application.feature.handlers.command_handler.update_walk_test_status_command_handler import \
    UpdateWalkTestStatusCommandHandler
from app.application.feature.handlers.query_handler.check_entered_at_walk_test_query_handler import \
    CheckEnteredAtWalkTestQueryHandler
from app.application.feature.handlers.query_handler.get_all_complaint_type_query_handler import \
    GetAllComplaintTypeQueryHandler
from app.application.feature.handlers.query_handler.get_all_problematic_service_type_query_handler import \
    GetAllProblematicServiceTypeQueryHandler
from app.application.feature.handlers.query_handler.get_all_service_type_query_handler import GetAllServiceTypeQueryHandler
from app.application.feature.handlers.query_handler.get_all_speed_test_servers_query_handler import \
    GetAllSpeedTestServersQueryHandler
from app.application.feature.handlers.query_handler.get_all_technology_types_query_handler import \
    GetAllTechnologyTypesQueryHandler
from app.application.feature.handlers.query_handler.get_all_test_step_type_query_handler import \
    GetAllTestStepTypeQueryHandler
from app.application.feature.handlers.query_handler.get_device_info_by_walk_test_id_query_handler import \
    GetDeviceInfoByWalkTestIdQueryHandler
from app.application.feature.handlers.query_handler.get_walk_test_by_msisdn_query_handler import \
    GetWalkTestByMSISDNQueryHandler
from app.application.feature.handlers.query_handler.get_walk_test_coordinates_query_handler import \
    GetWalkTestCoordinatesQueryHandler
from app.application.feature.handlers.query_handler.get_walk_test_results_by_walk_test_id_query_handler import \
    GetWalkTestResultsByWalkTestIdQueryHandler
from app.application.feature.handlers.query_handler.validate_walk_test_time_duration_query_handler import \
    ValidateWalkTestTimeDurationQueryHandler
from app.application.feature.queries.check_entered_at_walk_test_query import CheckEnteredAtWalkTestQuery
from app.application.feature.queries.get_all_complaint_type_query import GetAllComplaintTypeQuery
from app.application.feature.queries.get_all_problematic_service_type_query import GetAllProblematicServiceTypeQuery
from app.application.feature.queries.get_all_service_type_query import GetAllServiceTypeQuery
from app.application.feature.queries.get_all_speed_test_servers_query import GetAllSpeedTestServersQuery
from app.application.feature.queries.get_all_technology_types_query import GetAllTechnologyTypesQuery
from app.application.feature.queries.get_all_test_step_type_query import GetAllTestStepTypeQuery
from app.application.feature.queries.get_device_info_by_walk_test_id_query import GetDeviceInfoByWalkTestIdQuery
from app.application.feature.queries.get_walk_test_by_msisdn_query import GetWalkTestByMSISDNQuery
from app.application.feature.queries.get_walk_test_coordinates_query import GetWalkTestCoordinatesQuery
from app.application.feature.queries.get_walk_test_results_by_walk_test_id_query import GetWalkTestResultsByWalkTestIdQuery
from app.application.feature.queries.validate_walk_test_time_duration_query import ValidateWalkTestTimeDurationQuery
from app.application.mediator import Mediator
from app.domain.cache.cache_gateway import CacheGateway
from app.domain.repositories.users_repository import UsersRepository
from app.domain.services.get_ip_info_service import GetIpInfoService
from app.infrastructure.di.redis_client import get_cache
from app.infrastructure.di.repositories import get_users_repository, get_read_walk_test_repository, \
    get_write_walk_test_repository, get_read_technology_type_repository, get_read_complaint_type_repository, \
    get_read_problematic_service_type_repository, get_read_service_type_repository, get_read_test_step_type_repository, \
    get_write_device_info_repository, get_write_walk_test_results_unit_of_work, get_read_walk_test_results_repository, \
    get_read_device_info_repository, get_write_speed_test_servers_repository, get_read_speed_test_server_repository

from app.infrastructure.di.services import get_ip_info_service


def get_mediator(
        cache_gateway: CacheGateway = Depends(get_cache),
        ip_info_service: GetIpInfoService = Depends(get_ip_info_service),
        users_repository: UsersRepository = Depends(get_users_repository),
        read_walk_test_repository=Depends(get_read_walk_test_repository),
        write_walk_test_repository=Depends(get_write_walk_test_repository, ),
        write_device_info_repository=Depends(get_write_device_info_repository, ),
        write_speed_test_repository=Depends(get_write_speed_test_servers_repository),
        write_walk_test_results_unit_of_work=Depends(get_write_walk_test_results_unit_of_work),
        read_technology_repository=Depends(get_read_technology_type_repository, ),
        read_complaint_type_repository=Depends(get_read_complaint_type_repository),
        read_problematic_service_repository=Depends(get_read_problematic_service_type_repository),
        read_service_type_repository=Depends(get_read_service_type_repository),
        read_test_step_type_repository=Depends(get_read_test_step_type_repository),
        read_walk_test_results_by_walk_test_id_repository=Depends(get_read_walk_test_results_repository),
        read_device_info_repository=Depends(get_read_device_info_repository),
        read_speed_test_servers_repository=Depends(get_read_speed_test_server_repository),

) -> Mediator:
    # commands
    mediator = Mediator()
    mediator.register_handler(AuthenticateCommand,
                              AuthenticateCommandHandler(ip_info_service, cache_gateway=cache_gateway))
    mediator.register_handler(CreateUserCommand,
                              CreateUserCommandHandler(users_repository, cache_gateway=cache_gateway))
    mediator.register_handler(CreateWalkTestCommand,
                              CreateWalkTestCommandHandler(write_walk_test_repository, cache_gateway=cache_gateway))
    mediator.register_handler(UpdateDeviceInfoCommand,
                              UpdateDeviceInfoCommandHandler(write_device_info_repository=write_device_info_repository,
                                                             cache_gateway=cache_gateway))
    mediator.register_handler(CreateWalkTestResultsCommand, CreateWalkTestResultsCommandHandler(
        write_walk_test_result_unit_of_work=write_walk_test_results_unit_of_work, cache_gateway=cache_gateway))
    mediator.register_handler(UpdateWalkTestStatusCommand,
                              UpdateWalkTestStatusCommandHandler(write_walk_test_repository=write_walk_test_repository,
                                                                 cache_gateway=cache_gateway))
    mediator.register_handler(UpdateSpeedTestServersCommand, UpdateSpeedTestServersCommandHandler(
        write_speed_test_server_repository=write_speed_test_repository, cache_gateway=cache_gateway))
    mediator.register_handler(UpdateEnteredAtWalkTestCommand, UpdateEnteredAtWalkTestCommandHandler(write_walk_test_repository=write_walk_test_repository,cache_gateway=cache_gateway))

    # queries
    mediator.register_handler(GetWalkTestByMSISDNQuery,
                              GetWalkTestByMSISDNQueryHandler(read_walk_test_repository, cache_gateway=cache_gateway,
                                                              expire=3600))
    mediator.register_handler(GetAllTechnologyTypesQuery,
                              GetAllTechnologyTypesQueryHandler(read_technology_repository, cache_gateway=cache_gateway,
                                                                expire=3600))
    mediator.register_handler(GetAllComplaintTypeQuery, GetAllComplaintTypeQueryHandler(read_complaint_type_repository,
                                                                                        cache_gateway=cache_gateway,
                                                                                        expire=3600))
    mediator.register_handler(GetAllProblematicServiceTypeQuery,
                              GetAllProblematicServiceTypeQueryHandler(read_problematic_service_repository,
                                                                       cache_gateway=cache_gateway, expire=3600))
    mediator.register_handler(GetAllServiceTypeQuery,
                              GetAllServiceTypeQueryHandler(read_service_type_repository, cache_gateway=cache_gateway,
                                                            expire=3600))
    mediator.register_handler(GetAllTestStepTypeQuery, GetAllTestStepTypeQueryHandler(read_test_step_type_repository,
                                                                                      cache_gateway=cache_gateway,
                                                                                      expire=3600))
    mediator.register_handler(GetWalkTestResultsByWalkTestIdQuery, GetWalkTestResultsByWalkTestIdQueryHandler(
        read_walk_test_results_by_walk_test_id_repository, cache_gateway=cache_gateway, expire=3600))
    mediator.register_handler(GetDeviceInfoByWalkTestIdQuery,
                              GetDeviceInfoByWalkTestIdQueryHandler(read_device_info_repository,
                                                                    cache_gateway=cache_gateway, expire=3600))

    mediator.register_handler(GetAllSpeedTestServersQuery,
                              GetAllSpeedTestServersQueryHandler(read_speed_test_servers_repository,
                                                                 cache_gateway=cache_gateway, expire=3600))

    mediator.register_handler(CheckEnteredAtWalkTestQuery,CheckEnteredAtWalkTestQueryHandler(read_walk_test_repository,cache_gateway=cache_gateway,expire=3600))
    mediator.register_handler(GetWalkTestCoordinatesQuery,GetWalkTestCoordinatesQueryHandler(read_walk_test_repository,cache_gateway=cache_gateway,expire=3600))
    mediator.register_handler(ValidateWalkTestTimeDurationQuery,ValidateWalkTestTimeDurationQueryHandler(read_walk_test_repository,cache_gateway=cache_gateway,expire=3600))

    return mediator

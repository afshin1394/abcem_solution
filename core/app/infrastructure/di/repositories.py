from app.domain.repositories.read.read_complaint_type_repository import ReadComplaintTypeRepository
from app.domain.repositories.read.read_device_info_repository import ReadDeviceInfoRepository
from app.domain.repositories.read.read_problematic_service_repository import ReadProblematicServiceRepository
from app.domain.repositories.read.read_service_type_repository import ReadServiceTypeRepository
from app.domain.repositories.read.read_speed_test_server_repository import ReadSpeedTestServerRepository
from app.domain.repositories.read.read_technology_repository import ReadTechnologyRepository
from app.domain.repositories.read.read_test_step_type_repository import ReadTestStepTypeRepository
from app.domain.repositories.read.read_walk_test_repository import ReadWalkTestRepository
from app.domain.repositories.read.read_walk_test_results_repository import ReadWalkTestResultsRepository
from app.domain.repositories.users_repository import UsersRepository
from app.domain.repositories.write.multi.write_walk_test_result_unit_of_work import WriteWalkTestResultUnitOfWork
from app.domain.repositories.write.single.write_device_info_repository import WriteDeviceInfoRepository
from app.domain.repositories.write.single.write_speed_test_server_repository import WriteSpeedTestServerRepository
from app.domain.repositories.write.single.write_walk_test_repository import WriteWalkTestRepository
from app.infrastructure.di.database import get_db
from app.infrastructure.repository_impl.read.read_complaint_type_repository_impl import ReadComplaintTypeRepositoryImpl
from app.infrastructure.repository_impl.read.read_device_info_repository_impl import ReadDeviceInfoRepositoryImpl
from app.infrastructure.repository_impl.read.read_problematic_service_repository_impl import \
    ReadProblematicServiceRepositoryImpl
from app.infrastructure.repository_impl.read.read_service_type_repsitory_impl import ReadServiceTypeRepositoryImpl
from app.infrastructure.repository_impl.read.read_speed_test_server_repository_impl import \
    ReadSpeedTestServerRepositoryImpl
from app.infrastructure.repository_impl.read.read_technology_repository_impl import ReadTechnologyRepositoryImpl
from app.infrastructure.repository_impl.read.read_test_step_type_repositroy_impl import ReadTestStepTypeRepositoryImpl
from app.infrastructure.repository_impl.read.read_walk_test_repository_impl import ReadWalkTestRepositoryImpl
from app.infrastructure.repository_impl.read.read_walk_test_results_repository_impl import \
    ReadWalkTestResultsRepositoryImpl
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.infrastructure.repository_impl.users_repository_impl import UsersRepositoryImpl
from app.infrastructure.repository_impl.write.multi.write_walk_test_result_unit_of_work_impl import \
    WriteWalkTestResultsUnitOfWorkImpl
from app.infrastructure.repository_impl.write.single.write_device_info_repository_impl import  WriteDeviceInfoRepositoryImpl
from app.infrastructure.repository_impl.write.single.write_speed_test_server_repository_impl import \
    WriteSpeedTestServerRepositoryImpl
from app.infrastructure.repository_impl.write.single.write_walk_test_repository_impl import WriteWalkTestRepositoryImpl


async def get_speed_test_server_repository(
        async_session: AsyncSession = Depends(get_db),
) -> WriteSpeedTestServerRepository:
    return WriteSpeedTestServerRepositoryImpl(db=async_session)


async def get_users_repository(
        async_session: AsyncSession = Depends(get_db),
) -> UsersRepository:
    return UsersRepositoryImpl(db=async_session)


# write repos
async def get_write_walk_test_repository(
        async_session: AsyncSession = Depends(get_db),
) -> WriteWalkTestRepository:
    return WriteWalkTestRepositoryImpl(db=async_session)
async def get_write_speed_test_servers_repository(
        async_session: AsyncSession = Depends(get_db),
) -> WriteSpeedTestServerRepository:
    return WriteSpeedTestServerRepositoryImpl(db=async_session)

async def get_write_device_info_repository(
        async_session: AsyncSession = Depends(get_db)
) -> WriteDeviceInfoRepository:
    return WriteDeviceInfoRepositoryImpl(db=async_session)



# read repos
async def get_read_walk_test_results_repository(
    async_session: AsyncSession = Depends(get_db)
) -> ReadWalkTestResultsRepository:
    return ReadWalkTestResultsRepositoryImpl(db=async_session)


async def get_read_walk_test_repository(
        async_session: AsyncSession = Depends(get_db),
) -> ReadWalkTestRepository:
    return ReadWalkTestRepositoryImpl(db=async_session)


async def get_read_technology_type_repository(
        async_session: AsyncSession = Depends(get_db)
) -> ReadTechnologyRepository:
    return ReadTechnologyRepositoryImpl(db=async_session)

async def get_read_complaint_type_repository(
        async_session: AsyncSession = Depends(get_db)
) -> ReadComplaintTypeRepository:
    return ReadComplaintTypeRepositoryImpl(db=async_session)

async def get_read_problematic_service_type_repository(
        async_session: AsyncSession = Depends(get_db)
) -> ReadProblematicServiceRepository:
    return ReadProblematicServiceRepositoryImpl(db=async_session)

async def get_read_service_type_repository(
        async_session: AsyncSession = Depends(get_db)
) -> ReadServiceTypeRepository:
    return ReadServiceTypeRepositoryImpl(db=async_session)

async def get_read_test_step_type_repository(
        async_session: AsyncSession = Depends(get_db)
) -> ReadTestStepTypeRepository:
    return ReadTestStepTypeRepositoryImpl(db=async_session)

async def get_read_device_info_repository(
        async_session: AsyncSession = Depends(get_db)
) -> ReadDeviceInfoRepository:
    return ReadDeviceInfoRepositoryImpl(db=async_session)

async def get_read_speed_test_server_repository(
        async_session: AsyncSession = Depends(get_db)
) -> ReadSpeedTestServerRepository:
    return ReadSpeedTestServerRepositoryImpl(db=async_session)

# units of work
async def get_write_walk_test_results_unit_of_work(
        async_session: AsyncSession = Depends(get_db)
) -> WriteWalkTestResultUnitOfWork:
    return WriteWalkTestResultsUnitOfWorkImpl(db_session=async_session)







from app.domain.repositories.speed_test_repository import SpeedTestRepository
from fastapi import Depends

from app.infrastructure.di.repositories import get_speed_test_server_repository


async def run_speed_test_job(speed_test_repository : SpeedTestRepository = Depends(get_speed_test_server_repository)):
   pass
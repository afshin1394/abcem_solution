from fastapi import Depends
import asyncio

from app.application.usecase.speed_test_server_list_usecase import SpeedTestServerListUseCase
from app.infrastructure.di.usecases import get_speed_test_use_case


def schedule_speed_test_task(speed_test_use_case : SpeedTestServerListUseCase):
    """
    A wrapper function to resolve dependencies and execute the task.
    """
    async def run_task():
        await speed_test_use_case.execute(concurrency=3, retries=5)

    asyncio.run(run_task())

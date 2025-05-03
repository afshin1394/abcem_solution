from datetime import datetime
from typing import List

import pytz
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.walk_test_domain import WalkTestDomain
from app.domain.repositories.read.read_walk_test_repository import ReadWalkTestRepository
from app.infrastructure.mapper.mapper import map_models_list
from app.infrastructure.schemas.table_walk_test import TableWalkTest


class ReadWalkTestRepositoryImpl(ReadWalkTestRepository):


    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def validate_walk_test_execution_time(self,walk_test_id : str):
        result = await self.db.execute(
            select(TableWalkTest).where(TableWalkTest.id == walk_test_id)
        )
        print(f"result {result}")
        record  = result.scalars()
        print(f"record {record}")
        walk_test = record.first()
        print(f"walk_test {walk_test}")

        if not walk_test:
            return False  # or raise an exception

        entered_at = walk_test.entered_at
        print(f"entered_at {entered_at}")
        # Current time in Tehran timezone
        now_tehran = datetime.now(pytz.timezone("Asia/Tehran"))
        if entered_at is None:
            entered_at = now_tehran  # or handle missing timestamp

        print(f"entered_at {entered_at}")



        # If entered_at is timezone-aware, this is fine
        elapsed_seconds = (now_tehran - entered_at).total_seconds()
        print(f"elapsed_seconds {elapsed_seconds}")

        return elapsed_seconds < 300


    async def get_all_by_msisdn(self, msisdn: str) -> List[WalkTestDomain]:
        result = await self.db.execute(
            select(TableWalkTest).where(TableWalkTest.msisdn == msisdn).order_by(TableWalkTest.created_at.asc())
        )
        records = result.scalars().all()
        print(f"records {records.__str__()}")
        list_of_walk_test_domain = await map_models_list(records, WalkTestDomain)
        print(f"list_of_walk_test_domain {list_of_walk_test_domain.__str__()}")
        return list_of_walk_test_domain

    async def has_entered_at_value(self,walk_test_id : str) :
        result = await self.db.execute(
            select(TableWalkTest).where(TableWalkTest.id == walk_test_id)
        )

        record = result.scalars().one_or_none()
        print(f"record.entered_at is not None {record.entered_at}")
        if record.entered_at is not None:
            return True

        return False

    async def get_coordinates(self,walk_test_id : str) -> tuple[float, float]:
        result = await self.db.execute(
            select(TableWalkTest).where(TableWalkTest.id == walk_test_id)
        )
        record = result.scalars().one_or_none()
        return record.latitude, record.longitude

from datetime import datetime

import pytz
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.walk_test_domain import WalkTestDomain
from app.domain.enums.walk_test_state_enum import WalkTestStatusEnum
from app.domain.repositories.write.single.write_walk_test_repository import WriteWalkTestRepository
from app.infrastructure.mapper.mapper import map_models
from app.infrastructure.repository_impl.write import BaseWriteDB
from app.infrastructure.schemas.table_walk_test import TableWalkTest


class WriteWalkTestRepositoryImpl(BaseWriteDB, WriteWalkTestRepository):

    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def create_walk_test(self, walk_test_domain: WalkTestDomain) -> None:
        async with self:
            result = await map_models(walk_test_domain, TableWalkTest)
            self.db.add(result)

    async def update_walk_test_status(self, walk_test_id: str, walk_test_status: WalkTestStatusEnum):
        async with self:
            await self.db.execute(text("""
                UPDATE table_walk_test
                SET walk_test_status_id = :walk_test_status
                WHERE id = :walk_test_id
            """), {
                "walk_test_status": walk_test_status,
                "walk_test_id": walk_test_id
            })

    async def update_entered_at(self, walk_test_id: str):
        entered_at = datetime.now(pytz.timezone("Asia/Tehran"))
        async with self:
            await self.db.execute(text("""
                UPDATE table_walk_test
                SET entered_at = :entered_at
                WHERE id = :walk_test_id
            """), {
                "entered_at": entered_at,
                "walk_test_id": walk_test_id  # <-- match the SQL placeholder
            })

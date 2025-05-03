from app.domain.entities.users_domain import UserDomain
from app.domain.repositories.users_repository import UsersRepository
from app.infrastructure.mapper.mapper import map_models, map_models_list
from app.infrastructure.schemas.table_users import TableUsers
from sqlalchemy.ext.asyncio import AsyncSession


from sqlalchemy.future import select
from typing import List

class UsersRepositoryImpl(UsersRepository):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, user_domain: UserDomain) -> None:
        db_result = await map_models(user_domain, TableUsers)
        self.db.add(db_result)
        await self.db.commit()

    async def get_all(self) -> List[UserDomain]:
        # Execute query to fetch all rows from the table
        result = await self.db.execute(select(TableUsers))

        # Extract ORM models (SpeedTestTable instances)
        models = result.scalars().all()

        # Map ORM models to domain models
        return await map_models_list(models,UserDomain)

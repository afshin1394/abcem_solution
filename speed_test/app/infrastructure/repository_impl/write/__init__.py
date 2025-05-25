from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.exceptions import InfrastructureException, UniqueConstraintViolationException

class BaseWriteDB:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def commit(self):
        try:
            await self.db.commit()
        except IntegrityError as e:
                print("IntegrityError")
                error_message = str(e.orig)
                violated_key = error_message.split('Key ')[1].split('=')[0].strip('(').strip(')')
                violated_value = error_message.split('Key ')[1].split('=')[1].strip(')').strip()
                raise UniqueConstraintViolationException(key=violated_key, value=violated_value)
        except Exception as e:
            print("exception", e)
            raise InfrastructureException()

    async def rollback(self):
        await self.db.rollback()

    async def __aenter__(self):
        return self  # Enables `async with`

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit the async context manager, handling commit/rollback."""
        if exc_type:
            await self.rollback()
        else:
            await self.commit()
        await self.db.close()

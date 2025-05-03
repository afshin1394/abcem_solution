from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.exceptions import InfrastructureException, UniqueConstraintViolationException


class BaseWriteDB:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def commit(self):
        try:
            await self.db.commit()
        except IntegrityError as e:
            print("IntegrityError")
            error_message = str(e.orig)
            try:
                # Try parsing key and value
                key_value_part = error_message.split('Key ')[1]
                violated_key = key_value_part.split('=')[0].strip('(').strip(')')
                violated_value = key_value_part.split('=')[1].strip(')').strip()
                raise UniqueConstraintViolationException(key=violated_key, value=violated_value)
            except (IndexError, ValueError) as parse_error:
                # Parsing failed, raise with full original error message
                print(f"Parsing IntegrityError failed: {parse_error}",flush=True)
                print("exception", e, flush=True)

                raise InfrastructureException(message=error_message)
        except Exception as e:
            print("exception", e,flush=True)
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

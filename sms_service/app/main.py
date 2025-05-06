import asyncio
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from app.interfaces.api.endpoints import router_all
from fastapi import FastAPI
from app.core.config import settings
from app.infrastructure.consumers.sms_consumer import  RateLimitedConsumer
from app.infrastructure.rabbit import  get_rabbit
from alembic import command
from alembic.config import Config

from app.interfaces.dto.error_response import ErrorResponse
from app.interfaces.open_api import custom_openapi


async def my_event_handler(event: dict):
    print(f"External Event Handler: Received event {event} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return event

def run_migrations_blocking():
        alembic_cfg = Config("/app/alembic.ini")
        command.upgrade(alembic_cfg, "head")
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        print("🔧 Running Alembic migrations before startup...", flush=True)
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, func=run_migrations_blocking)
        print("✅ Alembic migrations finished.", flush=True)

        print("🔌 Connecting to RabbitMQ...", flush=True)
        connection = await get_rabbit()

        consumer = RateLimitedConsumer(
            connection=connection,
            max_event_per_second=settings.events_per_second,
            event_handler=my_event_handler
        )
        await consumer.start()

        app.state.rabbit_connection = connection
        app.state.consumer = consumer

        print("🚀 Consumer started successfully!", flush=True)
        yield

    except Exception as e:
        print(f'🚨 Exception during startup: {e}', flush=True)
        raise

    finally:
        print("🛑 Shutting down RabbitMQ connection...")
        if hasattr(app.state, "consumer"):
            await app.state.consumer.channel.close()
        if hasattr(app.state, "rabbit_connection"):
            await app.state.rabbit_connection.close()
        print("✅ RabbitMQ connection closed.", flush=True)

app = FastAPI(docs_url="/api/docs", redoc_url="/api/redoc", lifespan=lifespan)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Format the list of errors as needed
    errors = [f"{'.'.join(map(str, err['loc']))}: {err['msg']}" for err in exc.errors()]
    return ErrorResponse(
        status_code=422,
        content={
            "message": "Validation error",
            "code": 422,
            "errors": errors
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    # Optional: Log the exception details here
    return ErrorResponse(
        status_code=500,
        content={
            "message": "An unexpected error occurred",
            "code": 500,
            "errors": [str(exc)]
        },
    )



app.include_router(router_all)
app.openapi_schema = custom_openapi(app=app)

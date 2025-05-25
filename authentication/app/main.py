from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request

from app.application.exception import ApplicationException
from app.core.config import settings
from app.domain.exceptions import DomainException
from app.infrastructure.exceptions import InfrastructureException
from app.infrastructure.logto import seed_logto_resources_and_roles
from app.interfaces.dto.error_response import ErrorResponse

from app.interfaces.open_api import custom_openapi
from app.interfaces.api import router as login_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await seed_logto_resources_and_roles(settings.logto_json_path)
    except Exception as e:
        raise RuntimeError("Logto initialization failed") from e  # Stops app startup
    else:
        yield
app = FastAPI(docs_url="/api/docs", redoc_url="/api/redoc" , lifespan=lifespan)



@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return ErrorResponse(
        status_code=exc.status_code,
        content={
            "message": exc.detail if isinstance(exc.detail, str) else "HTTP Error occurred",
            "code": exc.status_code,
            "errors": [str(exc.detail)] if isinstance(exc.detail, str) else []
        },
    )
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


@app.exception_handler(DomainException)
async def domain_exception_handler(request: Request, exc: DomainException):
    return ErrorResponse(status_code=exc.status_code, content={
        "message": exc.message,
        "code": exc.status_code,
    }, )
@app.exception_handler(InfrastructureException)
async def domain_exception_handler(request: Request, exc: InfrastructureException):
    return ErrorResponse(status_code=exc.error_code, content={
        "message": exc.message,
        "code": exc.error_code,
    }, )
@app.exception_handler(ApplicationException)
async def domain_exception_handler(request: Request, exc: ApplicationException):
    return ErrorResponse(status_code=exc.error_code, content={
        "message": exc.message,
        "code": exc.error_code,
    }, )

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


app.include_router(login_router)
app.openapi_schema = custom_openapi(app=app)

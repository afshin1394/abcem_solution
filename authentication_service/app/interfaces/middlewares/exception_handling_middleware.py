# middleware/error_handling.py
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request,status
from fastapi.responses import JSONResponse
import logging
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import ValidationError

from app.infrastructure.exceptions import InfrastructureException
from app.interfaces.dto.response.base_response import BaseResponse
import time


class ExceptionHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            start_time = time.perf_counter()
            response = await call_next(request)
            process_time = time.perf_counter() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            return response
        except StarletteHTTPException as http_exc:
            response_dto = BaseResponse()
            response_dto.on_error(http_exc.status_code, http_exc.detail)
            return JSONResponse(status_code=http_exc.status_code, content=response_dto.model_dump())

        except ValidationError as validation_error:
            # Handle Pydantic validation errors
            response_dto = BaseResponse()
            response_dto.on_error(status.HTTP_422_UNPROCESSABLE_ENTITY, "Validation Error")

            return JSONResponse(status_code=422, content=response_dto.model_dump())
        except InfrastructureException as infra_exc:
            # Handle Pydantic validation errors
            response_dto = BaseResponse()
            response_dto.on_error(infra_exc.error_code, infra_exc.message)
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=response_dto.model_dump())

        except Exception as exc:
            # Handle generic unhandled exceptions
            logging.error(f"Unhandled exception: {exc}")
            response_dto = BaseResponse()
            response_dto.on_error(500, "Unhandled exception")
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=response_dto.model_dump())

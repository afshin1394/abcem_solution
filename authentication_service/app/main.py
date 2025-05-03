
from fastapi import FastAPI

from app.interfaces.middlewares.exception_handling_middleware import ExceptionHandlingMiddleware

from app.interfaces.api.v1.endpoints.login import router

app = FastAPI(docs_url="/api/docs", redoc_url="/api/redoc")
app.add_middleware(ExceptionHandlingMiddleware)

app.include_router(router)


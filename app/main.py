from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.core.exceptions import AppBaseException
from app.core.exception_handler import custom_exc_handler, validation_exc_handler
from app.core.middleware import LoggingMiddleware
from app.routers.auth_router import router as auth_router
from app.routers.client_router import router as client_router
from app.routers.user_router import router as user_router

app = FastAPI()

app.add_exception_handler(AppBaseException, custom_exc_handler)
app.add_exception_handler(RequestValidationError, validation_exc_handler)

app.add_middleware(LoggingMiddleware)

app.include_router(auth_router)
app.include_router(client_router)
app.include_router(user_router)
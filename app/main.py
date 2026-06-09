from fastapi import FastAPI

from app.core.middleware import LoggingMiddleware

app = FastAPI()

app.add_middleware(LoggingMiddleware)
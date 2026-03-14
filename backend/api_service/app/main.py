from fastapi import FastAPI
from app.routes.jobs import router
from app.logging_config import setup_logging

setup_logging()

app = FastAPI()
app.include_router(router)
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

from routers.web import web_router
from routers.api import mistral_router
from config.logger import logger

app = FastAPI(title="Mistral Property Assistant")

@app.on_event("startup")
async def startup_event():
    logger.info("Application starting up...")

# Mount Static Files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(BASE_DIR, "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Include Routers
app.include_router(web_router)
app.include_router(mistral_router, prefix="/api")


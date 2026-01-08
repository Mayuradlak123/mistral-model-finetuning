from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import os

web_router = APIRouter()

# Setup templates
# Relative path from this file: ../templates
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@web_router.get("/")
async def get_dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
from Backend.common.config import conf
from Backend.api import airInfo_json
from Backend.api.airInfo_json import call_api
from Backend.api.disease import call_diease

router = APIRouter()

config = conf()
dashboard = Jinja2Templates(directory=config.DASHBOARD)

@router.get("/dashboard", response_class=HTMLResponse, tags=["dashBoard"])
def index(request : Request):
    context = {
        'request' : request,
        'items' : call_api(),
        'disease' : call_diease()
    }
    return dashboard.TemplateResponse('index.html', context)

@router.get("/dashboard/tables", response_class=HTMLResponse, tags=["dashBoard"])
def index(request : Request):
    context = {
        'request' : request,
        'items' : call_api()
    }
    return dashboard.TemplateResponse('tables.html', context)

@router.get("/dashboard/charts", response_class=HTMLResponse, tags=["dashBoard"])
def index(request : Request):
    context = {
        'request' : request,
        'items' : call_api(),
        'disease' : call_diease()
    }
    return dashboard.TemplateResponse('charts.html', context)
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
from Backend.common.config import conf
from Backend.api.airInfo_json import json_list
from Backend.api.disease import json_list_disease

router = APIRouter()

config = conf()
dashboard = Jinja2Templates(directory=config.DASHBOARD)

@router.get("/dashboard", response_class=HTMLResponse)
def index(request : Request):
    context = {
        'request' : request,
        'items' : json_list,
        'disease' : json_list_disease
    }
    return dashboard.TemplateResponse('index.html', context)

@router.get("/dashboard/tables", response_class=HTMLResponse)
def index(request : Request):
    context = {
        'request' : request,
        'items' : json_list
    }
    return dashboard.TemplateResponse('tables.html', context)
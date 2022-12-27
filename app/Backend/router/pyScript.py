from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
from Backend.common.config import conf

router = APIRouter()

config = conf()
pyScript = Jinja2Templates(directory=config.PYSCRIPT)

@router.get("/pyScript", response_class=HTMLResponse, tags=["PyScript"])
def PyScript(request : Request):
    context = {
        'request' : request,
    }
    return pyScript.TemplateResponse('base.html', context)
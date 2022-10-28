from pipes import Template
from re import template
from typing import Union
from pathlib import Path
from fastapi import FastAPI, Response, Request
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from http import HTTPStatus



from scripts.setup import \
    app_desc, configs, meta_tags,\
     log_runtime, secrets

from scripts.struct import Basic_Mail, Text_Template, Pdf_Template
from scripts.auth import auth
from scripts.mail import send_basic_mail, send_template_mail
from scripts.pdf_engine import compile_from_tex

#from scripts.db import new_pdf_template


PATH_RT = Path(__file__).parent.parent.absolute()


log_runtime() # Store current ppid and pid in conf/runtime.yaml

app = FastAPI(
    title = 'Email Handler',
    description = app_desc,
    version = '0.0.1',
    contact = {
        'name': 'Jeremiah Carlson',
    },
    openapi_tags = meta_tags['tags']
)

app.add_middleware(
    CORSMiddleware,
    allow_origins = configs['cors']['allow_origins'],
    allow_credentials = configs['cors']['allow_credentials'],
    allow_methods = configs['cors']['allow_methods'],
    allow_headers = configs['cors']['allow_headers'],
)

app.mount("/static", StaticFiles(directory=PATH_RT / 'static'), name="static")
templates = Jinja2Templates(directory="static")

@app.get('/')
async def read_root(): # Redirect root to docs
    return RedirectResponse('/docs')

@app.get('/test1')
async def test(name: str, response: Response):
    filename = '%s.html' % name
    return FileResponse(PATH_RT / 'static' / 'html'/ filename)

'''
### DB Interactions ###
@app.post('/template/new')
async def post_template(payload: Pdf_Template,  request: Request, response: Response):
    if auth('basic', request.headers.get('x-api-key')):
        response.status_code = 200
        return (new_pdf_template(*payload.__dict__.values()))
    else:
        response.status_code = 401
        return 'Unauthorized'
'''


### --- --- ###


### Email ###
@app.post('/mail/basic', tags=['Basic Mail'])
async def send_mail(payload: Basic_Mail, request: Request, response: Response):
    if auth('basic', request.headers.get('x-api-key')):
        response.status_code = 200
        send_basic_mail(*payload.__dict__.values())
        return payload.__dict__
    else:
        response.status_code = 401
        return 'Unauthorized'

@app.post('/mail/template', tags=['Basic_Mail'])
async def send_mail(payload: Text_Template, request: Request, response: Response):
    if auth('basic', request.headers.get('x-api-key')):
        response.status_code = 200
        send_template_mail(*payload.__dict__.values())
        return payload.__dict__
    else:
        response.status_code = 401
        return 'Unauthorized'
### --- --- ###

if __name__ == '__main__':
    uvicorn.run(
        app,
        host='0.0.0.0' if configs['testing']['local_deploy'] else configs['deployment']['host'],
        port=configs['deployment']['port']
        )

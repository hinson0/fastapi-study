from fastapi import APIRouter, Form, Query, Request
from fastapi.templating import Jinja2Templates
import os

prod = os.getenv("PRODUCTION_MODE") == "1"
if prod:
    from data import creature as creature_data
else:
    from fake import creature as creature_data

templates = Jinja2Templates(directory="template")

router = APIRouter(prefix="/greet")


@router.get("/who2")
async def greet(name: str = Query(...)):
    """
    测试GET请求

    http -f get localhost:8000/greet/who2 name=yzb
    INFO:     127.0.0.1:57086 - "GET /greet/who2 HTTP/1.1" 200 OK
    HTTP/1.1 200 OK
    content-length: 25
    content-type: application/json
    date: Sat, 03 Jan 2026 23:40:26 GMT
    server: uvicorn

    {
        "message": "Hello, yzb!"
    }



    """
    return {"message": f"Hello, {name}!"}


@router.post("/who3")
async def greet_post(name: str = Form(...)):
    """
    测试POST请求

    (.venv) a114514@Mac cryptid % http -f post localhost:8000/greet/who3 name=yzb
    INFO:     127.0.0.1:57128 - "POST /greet/who3 HTTP/1.1" 200 OK
    HTTP/1.1 200 OK
    content-length: 25
    content-type: application/json
    date: Sat, 03 Jan 2026 23:41:20 GMT
    server: uvicorn

    {
        "message": "Hello, yzb!"
    }

    ##################################################################
    http -v post localhost:8000/greet/who3 name=yzb -f
    POST /greet/who3 HTTP/1.1
    Accept: application/json, */*
    Accept-Encoding: gzip, deflate
    Connection: keep-alive
    Content-Length: 13
    Content-Type: application/x-www-form-urlencoded
    Host: localhost:8000
    User-Agent: HTTPie/3.2.1
    """

    return {"message": f"Hello, {name}!"}


@router.get("/list")
async def list_creatures(request: Request):
    creatues = creature_data.get_all()

    return templates.TemplateResponse(
        "list.html", {"request": request, "creatues": creatues}
    )

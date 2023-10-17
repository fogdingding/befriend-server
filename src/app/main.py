import asyncio

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import (request_validation_exception_handler)
from fastapi.exceptions import RequestValidationError
from .schema.base import ApiException
from .router.v1.base import router as api_v1_router
from .model.sqlite.base import sqlite3_db as sqllite_db

app = FastAPI()


@app.exception_handler(ApiException)
async def unicorn_exception_handler(request: Request, exc: ApiException):
    error_callback = {
        "detail": {
            "msg": exc.msg,
            "body": exc.detail
        }
    }
    print({
        "code": exc.code,
        "callback": error_callback
    })
    return JSONResponse(status_code=exc.code, content=jsonable_encoder(error_callback))


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_detail = exc.errors()
    error_callback = {
        "detail": error_detail,
        "body": exc.body
    }
    print({
        "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
        "callback": error_callback
    })
    return await request_validation_exception_handler(request, exc)


@app.on_event("startup")
async def startup():
    print('startup')
    sqllite_db


@app.on_event("shutdown")
async def shutdown():
    print('down')


app.include_router(api_v1_router)


@app.get("/")
async def root():
    return {
        "message": "歡迎使用 Befriend API 服務，詳情請看 /docs"
    }

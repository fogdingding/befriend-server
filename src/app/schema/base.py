from typing import Union, List
from pydantic import BaseModel


class ApiException(Exception):
    def __init__(self,
                 code: int,
                 msg: str,
                 detail: dict = {}):
        self.code = code
        self.msg = msg
        self.detail = detail


class ApiErrorResponse(BaseModel):
    code: int = -1
    message: str = ""


class OrderQueryBase(BaseModel):
    field: str
    is_desc: bool = True

class TimeRangeQueryBase(BaseModel):
    start_time: Union[int, None] = None
    end_time: Union[int, None] = None


class DateRangeQueryBase(BaseModel):
    year: Union[str, None] = None
    month: Union[str, None] = None
    day: Union[str, None] = None


class PageQueryBase(BaseModel):
    page: int = 1
    size: Union[int, None] = 10
    order_by: Union[List[OrderQueryBase], None] = None

class PageQueryResultBase(BaseModel):
    total: int
    page: int
    size: Union[int, None]

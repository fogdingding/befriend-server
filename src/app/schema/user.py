from typing import Union, List
from pydantic import BaseModel


class UserBase(BaseModel):
    user_id: int
    username: str
    email: str
    nickname: str
    password: Union[str, None]
    img: Union[str, None]
    self_name: Union[str, None]
    first_name: Union[str, None]
    last_name: Union[str, None]
    introduction: Union[str, None]
    interest: Union[str, None]

class UserLoginInfo(UserBase):
    access_token: Union[str, None]
    token_type: str = "bearer"

class UserRegistrationQuery(BaseModel):
    username: str
    email: str
    nickname: str
    password: str

class UserRegistrationResult(BaseModel):
    is_success: bool
    msg: str

class UserLoginQuery(BaseModel):
    username: str
    password: str

class UserLoginResult(BaseModel):
    is_success: bool
    msg: str



class UserTrackQuery(BaseModel):
    track_user_id: int

class UserProfileQuery(BaseModel):
    email: str
    nickname: str
    img: Union[str, None]
    self_name: Union[str, None]
    first_name: Union[str, None]
    last_name: Union[str, None]
    introduction: Union[str, None]
    interest: Union[str, None]
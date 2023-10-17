from typing import Union, List, Dict
from fastapi import Depends, APIRouter, Request
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import schema
from ...controller.user import controller as user_controller
from ...schema import user as schema
from ...dependency import verify_user

router = APIRouter(prefix="/user",
                   tags=["user"],
                   responses={404: {
                       "description": "此頁面不存在喔, 嘻嘻"
                   }})

@router.post("/login", response_model=Union[schema.UserLoginInfo, None])
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()) -> Union[schema.UserLoginInfo, None]:
    return await user_controller.login(query=schema.UserLoginQuery(username=form_data.username, password=form_data.password))

@router.get("/list", response_model=Union[List[schema.UserBase], None])
async def get_user_list(request: Request, user: schema.UserLoginInfo = Depends(verify_user)) -> Union[List[schema.UserBase], None]:
    return await user_controller.get_users(is_all=True)

@router.get("/profile/{user_id}", response_model=Union[List[schema.UserBase], None])
async def get_profile(user_id: int, request: Request, user: schema.UserLoginInfo = Depends(verify_user)) -> Union[List[schema.UserBase], None]:
    return await user_controller.get_users(user_id=user_id, is_all=False)

@router.put("/profile", response_model=Union[bool, None])
async def put_profile(request: Request, query:schema.UserProfileQuery ,user: schema.UserLoginInfo = Depends(verify_user)) -> Union[bool, None]:
    return await user_controller.update_user(user_id=user.user_id, query=query)

@router.get("/track", response_model=Union[List[schema.UserBase], None])
async def get_track_users(request: Request, user: schema.UserLoginInfo = Depends(verify_user)) -> Union[List[schema.UserBase], None]:
    return await user_controller.get_track_users(user_id=user.user_id)

@router.post("/track", response_model=Union[bool, None])
async def track_user(request: Request, query: schema.UserTrackQuery, user: schema.UserLoginInfo = Depends(verify_user)) -> Union[bool, None]:
    return await user_controller.track_user(user_id=user.user_id, track_user_id=query.track_user_id)

@router.post("/registration", response_model=Union[schema.UserRegistrationResult, None])
async def registration(request: Request, query: schema.UserRegistrationQuery) -> Union[schema.UserRegistrationResult, None]:
    return await user_controller.registration(query=query)
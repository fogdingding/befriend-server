from typing import Union, List, Dict
from fastapi import Request
from ..schema import user as schema
from ..model.sqlite.user import user_db

class UserController:
    @staticmethod
    async def login(query: schema.UserLoginQuery) -> Union[schema.UserLoginInfo, None]:
        return await user_db.login(query)
    
    @staticmethod
    async def registration(query: schema.UserRegistrationQuery) -> Union[schema.UserRegistrationResult, None]:
        return await user_db.registration(query=query)
    
    @staticmethod
    async def get_users(user_id: int = 0, is_all: bool = True) -> Union[List[schema.UserBase], None]:
        return await user_db.get_users(user_id=user_id, is_all=is_all)
    
    @staticmethod
    async def get_track_users(user_id: int) -> Union[List[schema.UserBase], None]:
        return await user_db.get_track_users(user_id=user_id)
    
    @staticmethod
    async def track_user(user_id: int, track_user_id: int) -> Union[List[schema.UserBase], None]:
        return await user_db.track_user(user_id=user_id, track_user_id=track_user_id)
    
    @staticmethod
    async def update_user(user_id: int, query=schema.UserProfileQuery) -> Union[bool, None]:
        return await user_db.update_user(user_id=user_id, query=query)


controller = UserController()

import json
import uuid
import asyncio
import hashlib
import dateutil.parser as parser
from dateutil.relativedelta import relativedelta
from typing import Union, List, Dict, Tuple
from asyncpg import Record
from fastapi import Request
from datetime import datetime, timezone, timedelta
from ...schema import user as schema
from ...schema.base import ApiException
from ..config import get_settings
from .base import sqlite3_db


class UserModel:
    async def password_hash(self, password: str) -> str:
        password_hash = password.encode('utf-8')
        password_hash = hashlib.sha3_384(password_hash).hexdigest()
        return password_hash

    async def get_uuid(self) -> str:
        return str(uuid.uuid4()).replace('-', '')

    async def add_hour(self): 
        now = datetime.now()
        expired_time = now + timedelta(hours=1)
        return expired_time.strftime('%Y-%m-%d %H:%M:%S')

    async def login(self, query: schema.UserLoginQuery) -> Union[schema.UserLoginInfo, None]:
            try:
                password = await self.password_hash(password=query.password)
                conn = await sqlite3_db.get_conn()
                cursor = conn.cursor()

                cursor.execute('SELECT * FROM User WHERE username = ? and password = ?', (query.username, password,))
                row = cursor.fetchone()
                if len(row) > 0:
                    uuid_str = await self.get_uuid()
                    user = list(row)
                    user_id = user[0]
                    type_str = 'bearer'
                    expired_time = await self.add_hour()
                    cursor.execute('''INSERT INTO Expired (user_id, data, type, expired_time) 
                        VALUES (?, ?, ?, ?)''', 
                    (user_id, uuid_str, type_str, expired_time))
                    conn.commit()
                    conn.close()
                    return schema.UserLoginInfo(
                        user_id=user[0],
                        username=user[1],
                        email=user[2],
                        nickname=user[3],
                        password=None,
                        img=user[5],
                        self_name=user[6],
                        first_name=user[7],
                        last_name=user[8],
                        introduction=user[9],
                        interest=user[10],
                        access_token=uuid_str,
                    )
                else:
                    return None
            except Exception as e:
                raise ApiException(
                    code=500,
                    msg="DB操作發生非預期錯誤",
                    detail={
                        "payload": {
                            "username": query.username, 
                        },
                        "description": str(e)
                    }
                )

    async def verify_token(self, token: str) -> Union[schema.UserLoginInfo, None]:
        try:
            conn = await sqlite3_db.get_conn()
            cursor = conn.cursor()
            uuid_value = token
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute('''SELECT * FROM Expired WHERE data = ? AND type = 'bearer' AND expired_time >= ?''', 
                (uuid_value, current_time))
            row = cursor.fetchone()
            if row is None:
                return None
            else:
                row = list(row)
                user_id = row[1]
                cursor.execute('''SELECT * FROM User WHERE id = ?''', (user_id,))
                user = list(cursor.fetchone())
                return schema.UserLoginInfo(
                    user_id=user[0],
                    username=user[1],
                    email=user[2],
                    nickname=user[3],
                    password=None,
                    img=user[5],
                    self_name=user[6],
                    first_name=user[7],
                    last_name=user[8],
                    introduction=user[9],
                    interest=user[10],
                    access_token=uuid_value,
                )
        except Exception as e:
            raise ApiException(code=500,
                                msg="DB操作發生非預期錯誤",
                                detail={
                                    "payload": {
                                        "token": token
                                    },
                                    "description": str(e)
                                })

    async def registration(self, query: schema.UserRegistrationQuery) -> Union[schema.UserRegistrationResult, None]:
        try:
            conn = await sqlite3_db.get_conn()
            cursor = conn.cursor()
            
            # check exists user
            cursor.execute('SELECT * FROM User WHERE username = ?', (query.username,))
            row = cursor.fetchone()
            if row is None:
                # register user
                password = await self.password_hash(password=query.password)
                cursor.execute('INSERT INTO User (username, email, nickname, password) VALUES (?, ?, ?, ?)', 
                    (query.username, query.email, query.nickname, password))
                conn.commit()
                conn.close()
                return schema.UserRegistrationResult(is_success=True, msg='已經註冊完畢，請前往登入頁面~')
            else:
                return schema.UserRegistrationResult(is_success=False, msg='用戶名稱(帳戶)已被註冊過，請替換一個！')
        except Exception as e:
            raise ApiException(code=500,
                                msg="DB操作發生非預期錯誤",
                                detail={
                                    "payload": {
                                        'query': dict(query)
                                    },
                                    "description": str(e)
                                })

    async def get_users(self, user_id: int = 0, is_all=True) -> Union[List[schema.UserBase], None]:
        try:
            conn = await sqlite3_db.get_conn()
            cursor = conn.cursor()
            users = []
            users_append = users.append
            if is_all is True:
                cursor.execute('SELECT * FROM User', ())
                rows = cursor.fetchall()
                for row in rows:
                    user = list(row)
                    users_append(
                        schema.UserBase(
                        user_id=user[0],
                        username=user[1],
                        email=user[2],
                        nickname=user[3],
                        password=None,
                        img=user[5],
                        self_name=user[6],
                        first_name=user[7],
                        last_name=user[8],
                        introduction=user[9],
                        interest=user[10]
                        )
                    )
            else:
                cursor.execute('SELECT * FROM User WHERE id = ?', (user_id, ))
                row = cursor.fetchone()
                user = list(row)
                users_append(
                    schema.UserBase(
                    user_id=user[0],
                    username=user[1],
                    email=user[2],
                    nickname=user[3],
                    password=None,
                    img=user[5],
                    self_name=user[6],
                    first_name=user[7],
                    last_name=user[8],
                    introduction=user[9],
                    interest=user[10]
                    )
                )
            conn.close()
            return users
        except Exception as e:
            raise ApiException(code=500,
                                msg="DB操作發生非預期錯誤",
                                detail={
                                    "payload": {},
                                    "description": str(e)
                                })

    async def get_track_users(self, user_id) -> Union[List[schema.UserBase], None]:
        try:
            conn = await sqlite3_db.get_conn()
            cursor = conn.cursor()
            cursor.execute('''  SELECT U.*
                                FROM (
                                    SELECT DISTINCT user_id
                                    FROM log
                                    WHERE visit_user_id = ?
                                ) AS DistinctVisitors
                                JOIN User U ON DistinctVisitors.user_id = U.id;
                ''', (user_id,))
            rows = cursor.fetchall()
            users = []
            users_append = users.append
            for row in rows:
                user = list(row)
                if user_id == user[0]:
                    continue
                users_append(
                    schema.UserBase(
                    user_id=user[0],
                    username=user[1],
                    email=user[2],
                    nickname=user[3],
                    password=None,
                    img=user[5],
                    self_name=user[6],
                    first_name=user[7],
                    last_name=user[8],
                    introduction=user[9],
                    interest=user[10]
                    )
                )
            conn.close()
            return users
        except Exception as e:
            raise ApiException(code=500,
                                msg="DB操作發生非預期錯誤",
                                detail={
                                    "payload": {},
                                    "description": str(e)
                                })
    
    async def track_user(self, user_id: int, track_user_id: int) -> Union[bool, None]:
        try:
            conn = await sqlite3_db.get_conn()
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO log (user_id, visit_user_id) VALUES (?, ?)",
                (user_id, track_user_id)
            )
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            raise ApiException(code=500,
                                msg="DB操作發生非預期錯誤",
                                detail={
                                    "payload": {},
                                    "description": str(e)
                                })


    async def update_user(self, user_id: int, query: schema.UserProfileQuery) -> Union[bool, None]:
        try:
            conn = await sqlite3_db.get_conn()
            cursor = conn.cursor()
            user_data = {
                'user_id': user_id,
                'email': query.email,
                'nickname': query.nickname,
                'img': query.img,
                'self_name': query.self_name,
                'first_name': query.first_name,
                'last_name': query.last_name,
                'introduction': query.introduction,
                'interest': query.interest,
            }
            cursor.execute('''
                            UPDATE User 
                            SET email = :email,
                                nickname = :nickname,
                                img = :img,
                                self_name = :self_name,
                                first_name = :first_name,
                                last_name = :last_name,
                                introduction = :introduction,
                                interest = :interest
                            WHERE id = :user_id
                           ''', user_data)
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            raise ApiException(code=500,
                                msg="DB操作發生非預期錯誤",
                                detail={
                                    "payload": {},
                                    "description": str(e)
                                })
    
         
    async def sample(self, query: schema.UserRegistrationQuery) -> Union[schema.UserRegistrationResult, None]:
        try:
            conn = await sqlite3_db.get_conn()
            cursor = conn.cursor()
            
            # check exists user
            cursor.execute('SELECT * FROM User WHERE username = ?', (query.username,))
            row = cursor.fetchone()
            conn.close()
            return None
        except Exception as e:
            raise ApiException(code=500,
                                msg="DB操作發生非預期錯誤",
                                detail={
                                    "payload": {
                                        'query': dict(query)
                                    },
                                    "description": str(e)
                                })


user_db = UserModel()
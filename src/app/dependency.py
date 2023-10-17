import dateutil.parser as parser
from typing import Union, List
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .model.sqlite.user import user_db
from .schema import user as schema
from .schema.base import ApiException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/user/login")


async def verify_user(token: str = Depends(oauth2_scheme)) -> Union[schema.UserLoginInfo, None]:
    user = await user_db.verify_token(token)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
from typing import Annotated
from fastapi import Depends, HTTPException, Request
import jwt

from src.services.auth import AuthService
from src.db import async_session_maker

# repositories
from src.repositories.hotels import HotelsRepository
from src.repositories.rooms import RoomsRepository
from src.repositories.users import UsersRepository

def get_token(request: Request):
    """Get the token from the request"""
    token = request.cookies.get("access_token", None)
    if token:
        return token
    else:
        raise HTTPException(status_code=401, detail="Unauthenticated")

def get_current_user_id(token: str = Depends(get_token)) -> int:
    """Get the current user id from the request"""
    try:
        user_id = AuthService().decode_token(token)["id"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user_id

async def get_db():
    """Get the database session with context manager class"""
    async with DBManager() as db:
        yield db

# context manager for database session
class DBManager:
    def __init__(self):
        self.session = async_session_maker()

    async def __aenter__(self):
        self.rooms = RoomsRepository(self.session)
        self.hotels = HotelsRepository(self.session)
        self.users = UsersRepository(self.session)
        
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.session.rollback()
        await self.session.close()
    
    async def commit(self):
        await self.session.commit()

UserIdDep = Annotated[int, Depends(get_current_user_id)]
DBDep = Annotated[DBManager, Depends(get_db)]
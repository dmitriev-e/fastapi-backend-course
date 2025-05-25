import hashlib
from fastapi.openapi.models import Example
from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from src.repositories.users import UsersRepository
from src.db import async_session_maker
from src.schemas.users import UserAddToDB, UserRequestCreate

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

#   Helper function to hash password
def hash_password(password: str) -> str:
    """Hash a password"""
    return hashlib.sha256(password.encode()).hexdigest()


@router.post("/register")
async def register_user(
    data: UserRequestCreate = Body(
        openapi_examples={
            "User 1": Example(
                summary="Register a user test@example.com",
                value={"email": "test@example.com", "password": "password123"}
            ),
            "User 2": Example(
                summary="Register a user test2@example.com",
                value={"email": "test2@example.com", "password": "password123"}
            )
        }
    )
):
    """Register a new user"""

    #   Hash password and remove raw_password from data
    add_data = UserAddToDB(email=data.email, password=hash_password(data.raw_password))

    #   Add user to database
    async with async_session_maker() as session:
        user_added = await UsersRepository(session).add(add_data)
        await session.commit()

    #   Return response with added user data
    return JSONResponse(status_code=200, content={"detail": "User created", "data": user_added.model_dump()})

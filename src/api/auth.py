from fastapi.openapi.models import Example
from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from passlib.context import CryptContext

from src.repositories.users import UsersRepository
from src.db import async_session_maker
from src.schemas.users import UserAddToDB, UserRequestCreate, UserResponse

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

#   Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#   Helper function to hash password
def hash_password(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


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

    #   Check if user was added
    if user_added:
        #   Return response with added user data
        return JSONResponse(status_code=200, content={"detail": "User created", "data": user_added.model_dump()})
    else:
        #   Return response with error message
        return JSONResponse(status_code=400, content={"detail": "User not created", "data": None})

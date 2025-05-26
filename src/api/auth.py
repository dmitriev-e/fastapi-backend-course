import jwt
from datetime import datetime, timedelta, timezone
from fastapi.openapi.models import Example
from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from passlib.context import CryptContext

from src.services.auth import AuthService
from src.repositories.users import UsersRepository, UsersRepositoryLogin
from src.db import async_session_maker
from src.schemas.users import UserAddToDB, UserRequestCreate, UserRequestLogin

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

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
    add_data = UserAddToDB(email=data.email, password=AuthService().hash_password(data.raw_password))

    try:
    #   Add user to database
        async with async_session_maker() as session:
                user_added = await UsersRepository(session).add(add_data)
                await session.commit()
    except Exception as e:
        return JSONResponse(status_code=400, content={"detail": "User not created", "data": str(e.orig).split('\nDETAIL:')[1]})

    #   Check if user was added
    if user_added:
        #   Return response with added user data
        return JSONResponse(status_code=200, content={"detail": "User created", "data": user_added.model_dump()})
    else:
        #   Return response with error message
        return JSONResponse(status_code=400, content={"detail": "User not created", "data": None})


@router.post("/login")
async def login_user(
    data: UserRequestLogin = Body(
        openapi_examples={
            "User 1": Example(
                summary="Login a user test@example.com",
                value={"email": "test@example.com", "password": "password123"}
            )
        }
    )
):
    """Login a user"""

    async with async_session_maker() as session:
        user = await UsersRepositoryLogin(session).get_one_or_none(email=data.email)

    if not user or not AuthService().verify_password(data.raw_password, user.password):
        return JSONResponse(status_code=401, content={"detail": "Invalid credentials", "data": None})
    access_token = AuthService().create_access_token({"id": user.id})

    # Insert access token to cookies
    response = JSONResponse(status_code=200, content={"detail": "Login successful", "data": {"access_token": access_token}})
    response.set_cookie(key="access_token", value=access_token, secure=True, samesite="Strict")
    return response
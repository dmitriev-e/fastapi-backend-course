from datetime import datetime, timedelta, timezone
import jwt
from fastapi.openapi.models import Example
from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse

from passlib.context import CryptContext

from src.repositories.users import UsersRepository, UsersRepositoryLogin
from src.db import async_session_maker
from src.schemas.users import UserAddToDB, UserRequestCreate, UserRequestLogin

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

JWT_SECRET_KEY = "secret"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_TIME = 30

def create_access_token(data: dict) -> str:
    """Create an access token with expiration time"""
    to_encode = data.copy()
    to_encode.update({"exp": datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRATION_TIME)})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

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

    if not user or not pwd_context.verify(data.raw_password, user.password):
        return JSONResponse(status_code=401, content={"detail": "Invalid credentials", "data": None})
    access_token = create_access_token({"id": user.id})

    # Insert access token to cookies
    response = JSONResponse(status_code=200, content={"detail": "Login successful", "data": {"access_token": access_token}})
    response.set_cookie(key="access_token", value=access_token, secure=True, samesite="Strict")
    return response
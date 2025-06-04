from typing import Annotated
from fastapi import Depends, HTTPException, Request
import jwt

from src.services.auth import AuthService

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

UserIdDep = Annotated[int, Depends(get_current_user_id)]
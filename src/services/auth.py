import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext

from src.config import settings

JWT_EXPIRATION_TIME = 30

#   Auth service
class AuthService:
    """Auth service"""
    #   Password hashing context
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, data: dict) -> str:
        """Create an access token with expiration time"""
        to_encode = data.copy()
        to_encode.update({"exp": datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRATION_TIME)})
        return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    #   Helper function to hash password
    def hash_password(self, password: str) -> str:
        """Hash a password"""
        return self.pwd_context.hash(password)
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify a password"""
        return self.pwd_context.verify(password, hashed_password)


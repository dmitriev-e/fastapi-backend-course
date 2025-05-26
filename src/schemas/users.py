from pydantic import BaseModel, Field, EmailStr

class UserRequestCreate(BaseModel):
    email: EmailStr = Field(description="Email must be a valid email address", example="test@example.com")
    raw_password: str = Field(min_length=8, alias="password", description="Password must be at least 8 characters long", example="password123")

class UserRequestLogin(UserRequestCreate):
    pass

class UserResponse(BaseModel):
    id: int = Field(description="User ID", example=1)
    email: EmailStr

class UserAddToDB(BaseModel):
    email: EmailStr
    password: str

class UserResponseLogin(UserResponse):
    password: str

from pydantic import EmailStr, Field
from typing import Optional
from .base_schema import BaseSchema
from .user_schema import UserResponse

class SignupRequest(BaseSchema):
    email: EmailStr
    password: str = Field(
        ..., 
        min_length=8, 
        max_length=20,
        pattern=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,20}$"
    )
    nickname: str = Field(..., min_length=1, max_length=10)
    profileImageUrl: Optional[str] = None

class LoginRequest(BaseSchema):
    email: EmailStr
    password: str = Field(...)

class EmailAvailabilityResponse(BaseSchema):
    available: bool

class NicknameAvailabilityResponse(BaseSchema):
    available: bool

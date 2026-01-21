from pydantic import EmailStr, Field
from typing import Optional
from .base_schema import BaseSchema
from .user_schema import UserResponse

class SignupRequest(BaseSchema):
    email: EmailStr
    password: str = Field(..., min_length=8)
    nickname: str = Field(..., min_length=1)
    profileImageUrl: Optional[str] = None

class LoginRequest(BaseSchema):
    email: EmailStr
    password: str = Field(...)

class EmailAvailabilityResponse(BaseSchema):
    available: bool

class NicknameAvailabilityResponse(BaseSchema):
    available: bool

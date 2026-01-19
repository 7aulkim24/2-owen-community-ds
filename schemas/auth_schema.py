from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    nickname: str = Field(..., min_length=1)
    profile_image_url: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(...)

class UserResponse(BaseModel):
    user_id: str
    email: EmailStr
    nickname: str
    profile_image_url: Optional[str] = None
    created_at: str
    updated_at: Optional[str] = None

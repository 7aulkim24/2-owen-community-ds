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

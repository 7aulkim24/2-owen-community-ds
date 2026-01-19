from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

class PostCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)

class PostUpdateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)

class PostResponse(BaseModel):
    post_id: str
    title: str
    content: str
    author_id: str
    author_nickname: str
    created_at: str
    updated_at: Optional[str] = None
    view_count: int

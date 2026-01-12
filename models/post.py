from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PostRequest(BaseModel):
    """게시글 생성/수정 요청"""
    title: str
    content: str

class PostResponse(BaseModel):
    """게시글 응답"""
    post_id: int
    title: str
    content: str
    author_id: int
    author_nickname: str
    created_at: str
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True

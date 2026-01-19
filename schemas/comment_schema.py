from pydantic import BaseModel, Field
from typing import Optional

class CommentCreateRequest(BaseModel):
    content: str = Field(..., min_length=1)

class CommentUpdateRequest(BaseModel):
    content: str = Field(..., min_length=1)

class CommentResponse(BaseModel):
    comment_id: str
    post_id: str
    user_id: str
    user_nickname: str
    content: str
    created_at: str
    updated_at: Optional[str] = None

from pydantic import BaseModel, Field

class CommentCreateRequest(BaseModel):
    content: str = Field(..., min_length=1)

class CommentUpdateRequest(BaseModel):
    content: str = Field(..., min_length=1)

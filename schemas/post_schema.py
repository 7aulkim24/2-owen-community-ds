from pydantic import Field
from typing import Optional
from .base_schema import BaseSchema

class PostCreateRequest(BaseSchema):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)
    fileUrl: Optional[str] = None

class PostUpdateRequest(BaseSchema):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)
    fileUrl: Optional[str] = None

class PostAuthor(BaseSchema):
    userId: str
    nickname: str
    profileImageUrl: Optional[str] = None

class PostFile(BaseSchema):
    fileId: str
    fileUrl: str

class PostResponse(BaseSchema):
    postId: str
    title: str
    content: str
    likeCount: int = 0
    commentCount: int = 0
    hits: int = 0
    author: PostAuthor
    file: Optional[PostFile] = None
    createdAt: str
    updatedAt: Optional[str] = None
    isLiked: Optional[bool] = None

class PostImageUploadResponse(BaseSchema):
    postFileUrl: str

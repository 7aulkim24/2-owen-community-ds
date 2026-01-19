from fastapi import APIRouter, Depends, status, Query, UploadFile, File
from typing import Dict, List, Optional
from uuid import UUID
from utils.response import StandardResponse
from utils.error_codes import SuccessCode
from controllers.post_controller import post_controller
from schemas.post_schema import PostCreateRequest, PostUpdateRequest, PostResponse, PostImageUploadResponse
from schemas.base_schema import StandardResponse as StandardResponseSchema
from utils.auth_middleware import get_current_user

router = APIRouter(prefix="/v1/posts", tags=["게시글"])

@router.get("", response_model=StandardResponseSchema[List[PostResponse]], status_code=status.HTTP_200_OK)
async def get_posts(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """
    게시글 목록 조회
    - 모든 게시글을 최신순으로 반환
    - 인증 불필요
    """
    data = post_controller.getAllPosts(limit=limit, offset=offset)
    return StandardResponse.success(SuccessCode.POSTS_RETRIEVED, data)

@router.get("/{postId}", response_model=StandardResponseSchema[PostResponse], status_code=status.HTTP_200_OK)
async def get_post(postId: UUID):
    """
    게시글 상세 조회
    - 특정 게시글의 상세 정보 반환
    - 인증 불필요
    """
    data = post_controller.getPostById(postId)
    return StandardResponse.success(SuccessCode.POST_RETRIEVED, data)

@router.post("", response_model=StandardResponseSchema[PostResponse], status_code=status.HTTP_201_CREATED)
async def create_post(req: PostCreateRequest, user: Dict = Depends(get_current_user)):
    """
    게시글 생성
    - 인증된 사용자만 작성 가능
    """
    data = post_controller.createPost(req, user)
    return StandardResponse.success(SuccessCode.POST_CREATED, data)

@router.patch("/{postId}", response_model=StandardResponseSchema[PostResponse], status_code=status.HTTP_200_OK)
async def update_post(postId: UUID, req: PostUpdateRequest, user: Dict = Depends(get_current_user)):
    """
    게시글 수정
    - 작성자만 수정 가능
    """
    data = post_controller.updatePost(postId, req, user)
    return StandardResponse.success(SuccessCode.POST_UPDATED, data)

@router.delete("/{postId}", response_model=StandardResponseSchema[Dict], status_code=status.HTTP_200_OK)
async def delete_post(postId: UUID, user: Dict = Depends(get_current_user)):
    """
    게시글 삭제
    - 작성자만 삭제 가능
    """
    deletedPost = post_controller.deletePost(postId, user)
    return StandardResponse.success(
        SuccessCode.POST_DELETED, 
        {"postId": str(deletedPost["postId"]), "message": "게시글이 삭제되었습니다"}
    )

@router.post("/image", response_model=StandardResponseSchema[PostImageUploadResponse], status_code=status.HTTP_201_CREATED)
async def upload_post_image(postFile: UploadFile = File(...), user: Dict = Depends(get_current_user)):
    """
    게시글 이미지 업로드
    - 실무 역량 강화를 위해 Mock으로 구현 (추후 S3 연동 가능)
    """
    # 임시 URL 반환
    fileUrl = f"http://localhost:8000/public/image/post/{postFile.filename}"
    return StandardResponse.success(SuccessCode.POST_FILE_UPLOADED, {"postFileUrl": fileUrl})

@router.post("/{postId}/likes", response_model=StandardResponseSchema[Dict], status_code=status.HTTP_201_CREATED)
async def toggle_post_like(postId: UUID, user: Dict = Depends(get_current_user)):
    """
    게시글 좋아요 토글
    """
    data = post_controller.togglePostLike(postId, user["userId"])
    return StandardResponse.success(SuccessCode.POST_LIKE_UPDATED, data)

from fastapi import APIRouter, status, Request
from typing import Dict
from uuid import UUID
from utils.response import StandardResponse
from utils.error_codes import SuccessCode, ErrorCode
from utils.exceptions import UnauthorizedError
from controllers.post_controller import post_controller

router = APIRouter(prefix="/v1/posts", tags=["게시글"])

@router.get("", response_model=None, status_code=status.HTTP_200_OK)
async def get_posts():
    """
    게시글 목록 조회
    - 모든 게시글을 최신순으로 반환
    - 인증 불필요
    """
    data = post_controller.get_all_posts()
    return StandardResponse.success(SuccessCode.GET_POSTS_SUCCESS, data)

@router.get("/{post_id}", response_model=None, status_code=status.HTTP_200_OK)
async def get_post(post_id: UUID):
    """
    게시글 상세 조회
    - 특정 게시글의 상세 정보 반환
    - 인증 불필요
    """
    data = post_controller.get_post_by_id(post_id)
    return StandardResponse.success(SuccessCode.GET_POST_SUCCESS, data)

@router.post("", response_model=None, status_code=status.HTTP_201_CREATED)
async def create_post(req: Dict, request: Request):
    """
    게시글 생성
    - 인증된 사용자만 작성 가능
    - title, content 필수
    """
    if not request.state.user:
        raise UnauthorizedError(ErrorCode.UNAUTHORIZED)
    
    data = post_controller.create_post(req, request.state.user)
    return StandardResponse.success(SuccessCode.POST_CREATED, data, 201)

@router.patch("/{post_id}", response_model=None, status_code=status.HTTP_200_OK)
async def update_post(post_id: UUID, req: Dict, request: Request):
    """
    게시글 수정
    - 작성자만 수정 가능
    - title, content 수정 가능
    """
    if not request.state.user:
        raise UnauthorizedError(ErrorCode.UNAUTHORIZED)
        
    data = post_controller.update_post(post_id, req, request.state.user)
    return StandardResponse.success(SuccessCode.POST_UPDATED, data)

@router.delete("/{post_id}", response_model=None, status_code=status.HTTP_200_OK)
async def delete_post(post_id: UUID, request: Request):
    """
    게시글 삭제
    - 작성자만 삭제 가능
    """
    if not request.state.user:
        raise UnauthorizedError(ErrorCode.UNAUTHORIZED)
        
    deleted_post = post_controller.delete_post(post_id, request.state.user)
    return StandardResponse.success(
        SuccessCode.POST_DELETED, 
        {"post_id": deleted_post["post_id"], "message": "게시글이 삭제되었습니다"}
    )

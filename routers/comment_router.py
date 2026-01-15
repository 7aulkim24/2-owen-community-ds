from fastapi import APIRouter, status, Request
from typing import Dict
from uuid import UUID
from utils.response import StandardResponse
from utils.error_codes import SuccessCode, ErrorCode
from utils.exceptions import UnauthorizedError
from controllers.comment_controller import comment_controller

router = APIRouter(prefix="/v1/posts", tags=["댓글"])

@router.get("/{post_id}/comments", response_model=None, status_code=status.HTTP_200_OK)
async def get_comments(post_id: UUID):
    """
    댓글 목록 조회
    - 특정 게시글의 모든 댓글을 최신순으로 반환
    - 게시글이 존재하지 않으면 404 에러
    - 인증 불필요
    """
    data = comment_controller.get_comments_by_post(post_id)
    return StandardResponse.success(SuccessCode.COMMENTS_RETRIEVED, data)

@router.post("/{post_id}/comments", response_model=None, status_code=status.HTTP_201_CREATED)
async def create_comment(post_id: UUID, req: Dict, request: Request):
    """
    댓글 작성
    - 인증된 사용자만 작성 가능
    - content 필수
    - 게시글이 존재하지 않으면 404 에러
    """
    if not request.state.user:
        raise UnauthorizedError(ErrorCode.UNAUTHORIZED)
        
    data = comment_controller.create_comment(post_id, req, request.state.user)
    return StandardResponse.success(SuccessCode.COMMENT_CREATED, {"comment_id": data["comment_id"]}, 201)

@router.patch("/{post_id}/comments/{comment_id}", response_model=None, status_code=status.HTTP_200_OK)
async def update_comment(post_id: UUID, comment_id: UUID, req: Dict, request: Request):
    """
    댓글 수정
    - 작성자만 수정 가능
    - content 수정 가능
    - 게시글이나 댓글이 존재하지 않으면 404 에러
    """
    if not request.state.user:
        raise UnauthorizedError(ErrorCode.UNAUTHORIZED)
        
    data = comment_controller.update_comment(post_id, comment_id, req, request.state.user)
    return StandardResponse.success(SuccessCode.COMMENT_UPDATED, None)

@router.delete("/{post_id}/comments/{comment_id}", response_model=None, status_code=status.HTTP_200_OK)
async def delete_comment(post_id: UUID, comment_id: UUID, request: Request):
    """
    댓글 삭제
    - 작성자만 삭제 가능
    - 게시글이나 댓글이 존재하지 않으면 404 에러
    """
    if not request.state.user:
        raise UnauthorizedError(ErrorCode.UNAUTHORIZED)
        
    deleted_comment = comment_controller.delete_comment(post_id, comment_id, request.state.user)
    return StandardResponse.success(
        SuccessCode.COMMENT_DELETED,
        {"comment_id": deleted_comment["comment_id"], "message": "댓글이 삭제되었습니다"}
    )

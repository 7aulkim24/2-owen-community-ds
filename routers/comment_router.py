from fastapi import APIRouter, Depends, status
from typing import Dict, List, Optional
from uuid import UUID
from utils.response import StandardResponse
from utils.error_codes import SuccessCode
from controllers.comment_controller import comment_controller
from schemas.comment_schema import CommentCreateRequest, CommentUpdateRequest, CommentResponse
from schemas.base_schema import StandardResponse as StandardResponseSchema
from utils.auth_middleware import get_current_user

router = APIRouter(prefix="/v1/posts", tags=["댓글"])

@router.get("/{postId}/comments", response_model=StandardResponseSchema[List[CommentResponse]], status_code=status.HTTP_200_OK)
async def get_comments(postId: UUID):
    """
    댓글 목록 조회
    """
    data = comment_controller.getCommentsByPost(postId)
    return StandardResponse.success(SuccessCode.SUCCESS, data)

@router.post("/{postId}/comments", response_model=StandardResponseSchema[Dict], status_code=status.HTTP_201_CREATED)
async def create_comment(postId: UUID, req: CommentCreateRequest, user: Dict = Depends(get_current_user)):
    """
    댓글 작성
    """
    data = comment_controller.createComment(postId, req, user)
    return StandardResponse.success(SuccessCode.CREATED, {"commentId": str(data.commentId)})

@router.patch("/{postId}/comments/{commentId}", response_model=StandardResponseSchema[Optional[Dict]], status_code=status.HTTP_200_OK)
async def update_comment(postId: UUID, commentId: UUID, req: CommentUpdateRequest, user: Dict = Depends(get_current_user)):
    """
    댓글 수정
    """
    comment_controller.updateComment(postId, commentId, req, user)
    return StandardResponse.success(SuccessCode.UPDATED, None)

@router.delete("/{postId}/comments/{commentId}", response_model=StandardResponseSchema[Dict], status_code=status.HTTP_200_OK)
async def delete_comment(postId: UUID, commentId: UUID, user: Dict = Depends(get_current_user)):
    """
    댓글 삭제
    """
    deletedComment = comment_controller.deleteComment(postId, commentId, user)
    return StandardResponse.success(
        SuccessCode.DELETED,
        {"commentId": str(deletedComment["commentId"]), "message": "댓글이 삭제되었습니다"}
    )

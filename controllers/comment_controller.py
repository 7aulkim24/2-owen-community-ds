from typing import List, Dict, Union
from uuid import UUID
from models import comment_model, post_model, user_model
from utils.exceptions import APIError
from utils.error_codes import ErrorCode
from schemas.comment_schema import CommentCreateRequest, CommentUpdateRequest
from schemas.error_schema import ResourceError


class CommentController:
    """댓글 관련 비즈니스 로직"""

    def _formatComment(self, comment: Dict) -> Dict:
        """Comment 데이터를 API 응답 규격에 맞게 변환"""
        author = user_model.getUserById(comment["userId"])
        
        authorData = {
            "userId": comment["userId"],
            "nickname": comment["userNickname"],
            "profileImageUrl": author.get("profileImageUrl") if author else None
        }

        return {
            "commentId": comment["commentId"],
            "postId": comment["postId"],
            "content": comment["content"],
            "author": authorData,
            "createdAt": comment["createdAt"],
            "updatedAt": comment.get("updatedAt")
        }

    def getCommentsByPost(self, postId: Union[UUID, str]) -> List[Dict]:
        """특정 게시글의 댓글 목록 조회"""
        post = post_model.getPostById(postId)
        if not post:
            raise APIError(ErrorCode.POST_NOT_FOUND, ResourceError(resource="게시글", id=str(postId)))

        comments = comment_model.getCommentsByPost(postId)
        return [self._formatComment(c) for c in comments]

    def createComment(self, postId: Union[UUID, str], req: CommentCreateRequest, user: Dict) -> Dict:
        """댓글 작성"""
        post = post_model.getPostById(postId)
        if not post:
            raise APIError(ErrorCode.POST_NOT_FOUND, ResourceError(resource="게시글", id=str(postId)))

        commentData = comment_model.createComment(
            postId=postId,
            userId=user["userId"],
            userNickname=user["nickname"],
            content=req.content
        )

        return self._formatComment(commentData)

    def updateComment(self, postId: Union[UUID, str], commentId: Union[UUID, str], req: CommentUpdateRequest, user: Dict) -> Dict:
        """댓글 수정"""
        post = post_model.getPostById(postId)
        if not post:
            raise APIError(ErrorCode.POST_NOT_FOUND, ResourceError(resource="게시글", id=str(postId)))

        comment = comment_model.getCommentById(commentId)
        if not comment:
            raise APIError(ErrorCode.COMMENT_NOT_FOUND, ResourceError(resource="댓글", id=str(commentId)))

        if str(comment["postId"]) != str(postId):
            raise APIError(ErrorCode.COMMENT_NOT_FOUND, ResourceError(resource="댓글", id=str(commentId)))

        if str(comment["userId"]) != str(user["userId"]):
            raise APIError(ErrorCode.FORBIDDEN, ResourceError(resource="댓글"))

        updatedComment = comment_model.updateComment(
            commentId=commentId,
            content=req.content
        )

        return self._formatComment(updatedComment)

    def deleteComment(self, postId: Union[UUID, str], commentId: Union[UUID, str], user: Dict) -> Dict:
        """댓글 삭제"""
        post = post_model.getPostById(postId)
        if not post:
            raise APIError(ErrorCode.POST_NOT_FOUND, ResourceError(resource="게시글", id=str(postId)))

        comment = comment_model.getCommentById(commentId)
        if not comment:
            raise APIError(ErrorCode.COMMENT_NOT_FOUND, ResourceError(resource="댓글", id=str(commentId)))

        if str(comment["postId"]) != str(postId):
            raise APIError(ErrorCode.COMMENT_NOT_FOUND, ResourceError(resource="댓글", id=str(commentId)))

        if str(comment["userId"]) != str(user["userId"]):
            raise APIError(ErrorCode.FORBIDDEN, ResourceError(resource="댓글"))

        comment_model.deleteComment(commentId)

        return comment


comment_controller = CommentController()

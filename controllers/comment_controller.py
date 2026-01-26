from typing import List, Dict, Union
from models.comment_model import comment_model
from models.post_model import post_model
from models.user_model import user_model
from utils.exceptions import APIError
from utils.error_codes import ErrorCode
from schemas import CommentCreateRequest, CommentUpdateRequest, CommentResponse, CommentAuthor, ResourceError


class CommentController:
    """댓글 관련 비즈니스 로직"""

    def _formatComment(self, comment: Dict) -> CommentResponse:
        """Comment 데이터를 API 응답 규격에 맞게 변환"""
        author = user_model.getUserById(comment["userId"])
        
        # 최신 닉네임 우선 사용
        nickname = author.get("nickname") if author else comment["userNickname"]
        
        author_data = CommentAuthor(
            userId=comment["userId"],
            nickname=nickname,
            profileImageUrl=author.get("profileImageUrl") if author else None
        )

        return CommentResponse(
            commentId=comment["commentId"],
            postId=comment["postId"],
            content=comment["content"],
            author=author_data,
            createdAt=comment["createdAt"],
            updatedAt=comment.get("updatedAt")
        )

    def getCommentsByPost(self, postId: str) -> List[CommentResponse]:
        """특정 게시글의 댓글 목록 조회"""
        post = post_model.getPostById(postId)
        if not post:
            raise APIError(ErrorCode.POST_NOT_FOUND, ResourceError(resource="게시글", id=postId))

        comments = comment_model.getCommentsByPost(postId)
        return [self._formatComment(c) for c in comments]

    def createComment(self, postId: str, req: CommentCreateRequest, user: Dict) -> CommentResponse:
        """댓글 작성"""
        post = post_model.getPostById(postId)
        if not post:
            raise APIError(ErrorCode.POST_NOT_FOUND, ResourceError(resource="게시글", id=postId))

        comment_data = comment_model.createComment(
            postId=postId,
            userId=user["userId"],
            userNickname=user["nickname"],
            content=req.content
        )
        
        # 게시글의 댓글 수 캐시 업데이트
        post_model.updateCommentCount(postId, 1)

        return self._formatComment(comment_data)

    def updateComment(self, postId: str, commentId: str, req: CommentUpdateRequest, user: Dict) -> CommentResponse:
        """댓글 수정"""
        post = post_model.getPostById(postId)
        if not post:
            raise APIError(ErrorCode.POST_NOT_FOUND, ResourceError(resource="게시글", id=postId))

        comment = comment_model.getCommentById(commentId)
        if not comment:
            raise APIError(ErrorCode.COMMENT_NOT_FOUND, ResourceError(resource="댓글", id=commentId))

        if str(comment["postId"]) != postId:
            raise APIError(ErrorCode.COMMENT_NOT_FOUND, ResourceError(resource="댓글", id=commentId))

        if str(comment["userId"]) != str(user["userId"]):
            raise APIError(ErrorCode.FORBIDDEN, ResourceError(resource="댓글"))

        updated_comment = comment_model.updateComment(
            commentId=commentId,
            content=req.content
        )

        return self._formatComment(updated_comment)

    def deleteComment(self, postId: str, commentId: str, user: Dict) -> Dict:
        """댓글 삭제"""
        post = post_model.getPostById(postId)
        if not post:
            raise APIError(ErrorCode.POST_NOT_FOUND, ResourceError(resource="게시글", id=postId))

        comment = comment_model.getCommentById(commentId)
        if not comment:
            raise APIError(ErrorCode.COMMENT_NOT_FOUND, ResourceError(resource="댓글", id=commentId))

        if str(comment["postId"]) != postId:
            raise APIError(ErrorCode.COMMENT_NOT_FOUND, ResourceError(resource="댓글", id=commentId))

        if str(comment["userId"]) != str(user["userId"]):
            raise APIError(ErrorCode.FORBIDDEN, ResourceError(resource="댓글"))

        comment_model.deleteComment(commentId)
        
        # 게시글의 댓글 수 캐시 업데이트
        post_model.updateCommentCount(postId, -1)

        return comment


comment_controller = CommentController()

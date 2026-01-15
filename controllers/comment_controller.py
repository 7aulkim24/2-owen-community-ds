from typing import List, Dict, Union
from uuid import UUID
from models import comment_model, post_model
from utils.exceptions import NotFoundError, ForbiddenError, ValidationError
from utils.error_codes import ErrorCode

# --- Controller (Business Logic) ---
class CommentController:
    """댓글 관련 비즈니스 로직"""

    def __init__(self):
        pass

    def get_comments_by_post(self, post_id: Union[UUID, str]) -> List[Dict]:
        """특정 게시글의 댓글 목록 조회"""
        # 게시글 존재 여부 확인
        post = post_model.get_post_by_id(post_id)
        if not post:
            raise NotFoundError("게시글")

        # 댓글 목록 조회
        comments = comment_model.get_comments_by_post(post_id)
        return comments

    def create_comment(self, post_id: Union[UUID, str], req: Dict, user: Dict) -> Dict:
        """댓글 작성"""
        # 게시글 존재 여부 확인
        post = post_model.get_post_by_id(post_id)
        if not post:
            raise NotFoundError("게시글")

        # 입력값 검증
        content = req.get("content", "").strip()
        if not content:
            raise ValidationError(ErrorCode.EMPTY_CONTENT, {"field": "content"})

        # 댓글 생성
        comment_data = comment_model.create_comment(
            post_id=post_id,
            user_id=user["user_id"],
            user_nickname=user["nickname"],
            content=content
        )

        return comment_data

    def update_comment(self, post_id: Union[UUID, str], comment_id: Union[UUID, str], req: Dict, user: Dict) -> Dict:
        """댓글 수정"""
        # 게시글 존재 여부 확인
        post = post_model.get_post_by_id(post_id)
        if not post:
            raise NotFoundError("게시글")

        # 댓글 존재 여부 확인
        comment = comment_model.get_comment_by_id(comment_id)
        if not comment:
            raise NotFoundError("댓글")

        # 댓글이 해당 게시글에 속하는지 확인 (문자열로 비교)
        if str(comment["post_id"]) != str(post_id):
            raise NotFoundError("댓글")

        # 권한 확인 (작성자만 수정 가능)
        if str(comment["user_id"]) != str(user["user_id"]):
            raise ForbiddenError(ErrorCode.NOT_OWNER, {"resource": "댓글"})

        # 입력값 검증
        content = req.get("content", "").strip()
        if not content:
            raise ValidationError(ErrorCode.EMPTY_CONTENT, {"field": "content"})

        # 댓글 수정
        updated_comment = comment_model.update_comment(
            comment_id=comment_id,
            content=content
        )

        if not updated_comment:
            raise NotFoundError("댓글")

        return updated_comment

    def delete_comment(self, post_id: Union[UUID, str], comment_id: Union[UUID, str], user: Dict) -> Dict:
        """댓글 삭제"""
        # 게시글 존재 여부 확인
        post = post_model.get_post_by_id(post_id)
        if not post:
            raise NotFoundError("게시글")

        # 댓글 존재 여부 확인
        comment = comment_model.get_comment_by_id(comment_id)
        if not comment:
            raise NotFoundError("댓글")

        # 댓글이 해당 게시글에 속하는지 확인
        if str(comment["post_id"]) != str(post_id):
            raise NotFoundError("댓글")

        # 권한 확인 (작성자만 삭제 가능)
        if str(comment["user_id"]) != str(user["user_id"]):
            raise ForbiddenError(ErrorCode.NOT_OWNER, {"resource": "댓글"})

        # 댓글 삭제
        comment_model.delete_comment(comment_id)

        return comment


# 컨트롤러 인스턴스 생성
comment_controller = CommentController()

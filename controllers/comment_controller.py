from typing import List, Dict
from models import comment_model, post_model
from utils.exceptions import NotFoundError, ForbiddenError, ValidationError

# --- Controller (Business Logic) ---
class CommentController:
    """댓글 관련 비즈니스 로직"""

    def __init__(self):
        # 임시 사용자 정보 (인증 구현 전까지 하드코딩)
        self.MOCK_USER_ID = "user_001"
        self.MOCK_USER_NICKNAME = "테스트유저"

    def get_comments_by_post(self, post_id: str) -> List[Dict]:
        """특정 게시글의 댓글 목록 조회"""
        # 게시글 존재 여부 확인
        post = post_model.get_post_by_id(post_id)
        if not post:
            raise NotFoundError("게시글")

        # 댓글 목록 조회
        comments = comment_model.get_comments_by_post(post_id)
        return comments

    def create_comment(self, post_id: str, req: Dict) -> Dict:
        """댓글 작성"""
        # 게시글 존재 여부 확인
        post = post_model.get_post_by_id(post_id)
        if not post:
            raise NotFoundError("게시글")

        # 입력값 검증
        content = req.get("content", "").strip()
        if not content:
            raise ValidationError("EMPTY_CONTENT", {"field": "content"})

        # 댓글 생성
        comment_data = comment_model.create_comment(
            post_id=post_id,
            user_id=self.MOCK_USER_ID,
            user_nickname=self.MOCK_USER_NICKNAME,
            content=content
        )

        return comment_data

    def update_comment(self, post_id: str, comment_id: str, req: Dict) -> Dict:
        """댓글 수정"""
        # 게시글 존재 여부 확인
        post = post_model.get_post_by_id(post_id)
        if not post:
            raise NotFoundError("게시글")

        # 댓글 존재 여부 확인
        comment = comment_model.get_comment_by_id(comment_id)
        if not comment:
            raise NotFoundError("댓글")

        # 댓글이 해당 게시글에 속하는지 확인
        if comment["post_id"] != post_id:
            raise NotFoundError("댓글")

        # 권한 확인 (작성자만 수정 가능)
        if comment["user_id"] != self.MOCK_USER_ID:
            raise ForbiddenError("NOT_OWNER", {"resource": "댓글"})

        # 입력값 검증
        content = req.get("content", "").strip()
        if not content:
            raise ValidationError("EMPTY_CONTENT", {"field": "content"})

        # 댓글 수정
        updated_comment = comment_model.update_comment(
            comment_id=comment_id,
            content=content
        )

        if not updated_comment:
            raise NotFoundError("댓글")

        return updated_comment

    def delete_comment(self, post_id: str, comment_id: str) -> Dict:
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
        if comment["post_id"] != post_id:
            raise NotFoundError("댓글")

        # 권한 확인 (작성자만 삭제 가능)
        if comment["user_id"] != self.MOCK_USER_ID:
            raise ForbiddenError("NOT_OWNER", {"resource": "댓글"})

        # 댓글 삭제
        comment_model.delete_comment(comment_id)

        return comment


# 컨트롤러 인스턴스 생성
comment_controller = CommentController()

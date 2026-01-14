from typing import List, Dict
from datetime import datetime
from models import post_model
from utils.exceptions import PostNotFoundError, ForbiddenError, ValidationError
from utils.error_codes import ErrorCode

# --- Controller (Business Logic) ---
class PostController:
    """게시글 관련 비즈니스 로직"""
    def __init__(self):
        # Phase 3: Model 계층 사용
        # 임시 사용자 정보 (인증 구현 전까지 하드코딩)
        self.MOCK_USER_ID = "user_001"  # UUID 형식으로 변경
        self.MOCK_USER_NICKNAME = "테스트유저"

    def get_all_posts(self):
        """게시글 목록 조회 로직"""
        posts_data = post_model.get_posts()
        return posts_data

    def get_post_by_id(self, post_id: str):
        """게시글 상세 조회 로직"""
        post = post_model.get_post_by_id(post_id)
        if not post:
            raise PostNotFoundError(post_id)

        # 조회수 증가
        post_model.increment_view_count(post_id)

        return post

    def create_post(self, req: Dict):
        """게시글 생성 로직"""
        # 입력값 검증 (제목과 내용이 비어있는지 확인)
        title = req.get("title", "").strip()
        content = req.get("content", "").strip()

        if not title:
            raise ValidationError(ErrorCode.TITLE_TOO_SHORT, {"field": "title"})
        if not content:
            raise ValidationError(ErrorCode.EMPTY_CONTENT, {"field": "content"})

        # Model을 통해 게시글 생성
        post_data = post_model.create_post(
            title=title,
            content=content,
            author_id=self.MOCK_USER_ID,
            author_nickname=self.MOCK_USER_NICKNAME
        )

        return post_data

    def update_post(self, post_id: str, req: Dict):
        """게시글 수정 로직"""
        post = post_model.get_post_by_id(post_id)
        if not post:
            raise PostNotFoundError(post_id)

        # TODO: 세션 기반 권한 확인 로직 구현 (Phase 7)
        if post["author_id"] != self.MOCK_USER_ID:
            raise ForbiddenError(ErrorCode.NOT_OWNER, {"resource": "게시글"})

        # 입력값 검증
        title = req.get("title", "").strip()
        content = req.get("content", "").strip()

        if not title:
            raise ValidationError(ErrorCode.TITLE_TOO_SHORT, {"field": "title"})
        if not content:
            raise ValidationError(ErrorCode.EMPTY_CONTENT, {"field": "content"})

        # Model을 통해 게시글 수정
        updated_post = post_model.update_post(
            post_id=post_id,
            title=title,
            content=content
        )

        return updated_post

    def delete_post(self, post_id: str):
        """게시글 삭제 로직"""
        post = post_model.get_post_by_id(post_id)
        if not post:
            raise PostNotFoundError(post_id)

        # TODO: 세션 기반 권한 확인 로직 구현 (Phase 7)
        if post["author_id"] != self.MOCK_USER_ID:
            raise ForbiddenError(ErrorCode.NOT_OWNER, {"resource": "게시글"})

        # 게시글 삭제 시 관련 댓글들도 함께 삭제
        from models import comment_model
        deleted_comments_count = comment_model.delete_comments_by_post(post_id)

        # Model을 통해 게시글 삭제
        post_model.delete_post(post_id)

        return post

# 컨트롤러 인스턴스 생성
post_controller = PostController()



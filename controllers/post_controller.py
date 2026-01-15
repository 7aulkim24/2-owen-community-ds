from typing import List, Dict, Union
from datetime import datetime
from uuid import UUID
from models import post_model
from utils.exceptions import PostNotFoundError, ForbiddenError, ValidationError
from utils.error_codes import ErrorCode

# --- Controller (Business Logic) ---
class PostController:
    """게시글 관련 비즈니스 로직"""
    def __init__(self):
        pass

    def get_all_posts(self):
        """게시글 목록 조회 로직"""
        posts_data = post_model.get_posts()
        return posts_data

    def get_post_by_id(self, post_id: Union[UUID, str]):
        """게시글 상세 조회 로직"""
        post = post_model.get_post_by_id(post_id)
        if not post:
            raise PostNotFoundError(str(post_id))

        # 조회수 증가
        post_model.increment_view_count(post_id)

        return post

    def create_post(self, req: Dict, user: Dict):
        """게시글 생성 로직"""
        # 입력값 검증
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
            author_id=user["user_id"],
            author_nickname=user["nickname"]
        )

        return post_data

    def update_post(self, post_id: Union[UUID, str], req: Dict, user: Dict):
        """게시글 수정 로직"""
        post = post_model.get_post_by_id(post_id)
        if not post:
            raise PostNotFoundError(str(post_id))

        # 권한 확인 (작성자 확인)
        if str(post["author_id"]) != str(user["user_id"]):
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

    def delete_post(self, post_id: Union[UUID, str], user: Dict):
        """게시글 삭제 로직"""
        post = post_model.get_post_by_id(post_id)
        if not post:
            raise PostNotFoundError(str(post_id))

        # 권한 확인
        if str(post["author_id"]) != str(user["user_id"]):
            raise ForbiddenError(ErrorCode.NOT_OWNER, {"resource": "게시글"})

        # 게시글 삭제 시 관련 댓글들도 함께 삭제
        from models import comment_model
        comment_model.delete_comments_by_post(post_id)

        # Model을 통해 게시글 삭제
        post_model.delete_post(post_id)

        return post

# 컨트롤러 인스턴스 생성
post_controller = PostController()

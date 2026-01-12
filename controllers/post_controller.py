from typing import List
from datetime import datetime
from models.post import PostRequest, PostResponse
from utils.exceptions import NotFoundError, ForbiddenError

# --- Controller (Business Logic) ---
class PostController:
    def __init__(self):
        # 임시 메모리 저장소 (Phase 2: 딕셔너리 직접 사용)
        self.posts_db = {}
        self.next_post_id = 1
        # 임시 사용자 정보 (인증 구현 전까지 하드코딩)
        self.MOCK_USER_ID = 1
        self.MOCK_USER_NICKNAME = "테스트유저"

    def get_all_posts(self):
        """게시글 목록 조회 로직"""
        posts_list = sorted(self.posts_db.values(), key=lambda x: x["post_id"], reverse=True)
        return [
            PostResponse(
                post_id=post["post_id"],
                title=post["title"],
                content=post["content"],
                author_id=post["author_id"],
                author_nickname=post["author_nickname"],
                created_at=post["created_at"],
                updated_at=post.get("updated_at")
            ).dict()
            for post in posts_list
        ]

    def get_post_by_id(self, post_id: int):
        """게시글 상세 조회 로직"""
        if post_id not in self.posts_db:
            raise NotFoundError("게시글")
        
        post = self.posts_db[post_id]
        return PostResponse(**post).dict()

    def create_post(self, req: PostRequest):
        """게시글 생성 로직"""
        # 입력값 검증 (제목과 내용이 비어있는지 확인)
        if not req.title.strip():
            raise ForbiddenError("제목은 비어있을 수 없습니다")
        if not req.content.strip():
            raise ForbiddenError("내용은 비어있을 수 없습니다")
        
        post_id = self.next_post_id
        post_data = {
            "post_id": post_id,
            "title": req.title,
            "content": req.content,
            "author_id": self.MOCK_USER_ID,
            "author_nickname": self.MOCK_USER_NICKNAME,
            "created_at": datetime.now().isoformat(),
            "updated_at": None
        }
        
        self.posts_db[post_id] = post_data
        self.next_post_id += 1
        return PostResponse(**post_data).dict()

    def update_post(self, post_id: int, req: PostRequest):
        """게시글 수정 로직"""
        if post_id not in self.posts_db:
            raise NotFoundError("게시글")
        
        post = self.posts_db[post_id]
        
        # TODO: Phase 7에서 세션 기반 권한 확인 추가
        if post["author_id"] != self.MOCK_USER_ID:
            raise ForbiddenError("게시글 작성자만 수정할 수 있습니다")
        
        # 입력값 검증
        if not req.title.strip():
            raise ForbiddenError("제목은 비어있을 수 없습니다")
        if not req.content.strip():
            raise ForbiddenError("내용은 비어있을 수 없습니다")
        
        post["title"] = req.title
        post["content"] = req.content
        post["updated_at"] = datetime.now().isoformat()
        
        return PostResponse(**post).dict()

    def delete_post(self, post_id: int):
        """게시글 삭제 로직"""
        if post_id not in self.posts_db:
            raise NotFoundError("게시글")
        
        post = self.posts_db[post_id]
        
        # TODO: Phase 7에서 세션 기반 권한 확인 추가
        if post["author_id"] != self.MOCK_USER_ID:
            raise ForbiddenError("게시글 작성자만 삭제할 수 있습니다")
        
        return self.posts_db.pop(post_id)

# 컨트롤러 인스턴스 생성
post_controller = PostController()



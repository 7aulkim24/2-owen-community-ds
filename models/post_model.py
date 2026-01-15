from typing import Dict, List, Optional, Union
from datetime import datetime
from uuid import UUID, uuid4


class PostModel:
    """게시글 데이터 관리 Model"""

    def __init__(self):
        # 메모리 기반 게시글 저장소 (Key를 문자열로 관리하여 JSON 직렬화 호환성 확보)
        self.posts_db: Dict[str, Dict] = {}

    def _normalize_id(self, id_val: Union[UUID, str]) -> str:
        """UUID 객체 또는 문자열을 문자열 형식의 UUID로 정규화"""
        return str(id_val)

    def get_next_post_id(self) -> str:
        """다음 게시글 ID 생성 (문자열로 반환)"""
        return str(uuid4())

    def create_post(self, title: str, content: str, author_id: Union[UUID, str], author_nickname: str) -> Dict:
        """게시글 생성"""
        post_id = self.get_next_post_id()
        author_id_str = self._normalize_id(author_id)

        post_data = {
            "post_id": post_id,
            "title": title,
            "content": content,
            "author_id": author_id_str,
            "author_nickname": author_nickname,
            "created_at": datetime.now().isoformat(),
            "updated_at": None,
            "view_count": 0
        }

        self.posts_db[post_id] = post_data
        return post_data.copy()

    def get_posts(self, limit: int = 10, offset: int = 0) -> List[Dict]:
        """게시글 목록 조회 (페이징 지원)"""
        # 최신순 정렬
        posts_list = sorted(
            self.posts_db.values(),
            key=lambda x: x["created_at"],
            reverse=True
        )

        # 페이징 적용
        start_idx = offset
        end_idx = offset + limit
        return posts_list[start_idx:end_idx]

    def get_post_by_id(self, post_id: Union[UUID, str]) -> Optional[Dict]:
        """게시글 ID로 조회"""
        post_id_str = self._normalize_id(post_id)
        return self.posts_db.get(post_id_str)

    def increment_view_count(self, post_id: Union[UUID, str]) -> bool:
        """조회수 증가"""
        post_id_str = self._normalize_id(post_id)
        if post_id_str in self.posts_db:
            self.posts_db[post_id_str]["view_count"] += 1
            return True
        return False

    def update_post(self, post_id: Union[UUID, str], title: str, content: str) -> Optional[Dict]:
        """게시글 수정"""
        post_id_str = self._normalize_id(post_id)
        if post_id_str not in self.posts_db:
            return None

        post = self.posts_db[post_id_str]
        post["title"] = title
        post["content"] = content
        post["updated_at"] = datetime.now().isoformat()

        return post.copy()

    def delete_post(self, post_id: Union[UUID, str]) -> bool:
        """게시글 삭제"""
        post_id_str = self._normalize_id(post_id)
        if post_id_str in self.posts_db:
            del self.posts_db[post_id_str]
            return True
        return False

    def get_total_posts_count(self) -> int:
        """전체 게시글 수 조회"""
        return len(self.posts_db)

    def get_posts_by_author(self, author_id: Union[UUID, str]) -> List[Dict]:
        """특정 작성자의 게시글 조회"""
        author_id_str = self._normalize_id(author_id)
        return [post for post in self.posts_db.values() if post["author_id"] == author_id_str]

    def search_posts(self, keyword: str) -> List[Dict]:
        """게시글 검색 (제목+내용)"""
        keyword_lower = keyword.lower()
        return [
            post for post in self.posts_db.values()
            if keyword_lower in post["title"].lower() or keyword_lower in post["content"].lower()
        ]


# Model 인스턴스 생성
post_model = PostModel()

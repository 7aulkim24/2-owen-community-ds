from typing import Dict, List, Optional, Union
from datetime import datetime
from uuid import UUID, uuid4


class CommentModel:
    """댓글 데이터 관리 Model"""

    def __init__(self):
        # 메모리 기반 댓글 저장소 (Key를 문자열로 관리)
        self.comments_db: Dict[str, Dict] = {}

    def _normalize_id(self, id_val: Union[UUID, str]) -> str:
        """ID 정규화 (UUID 객체 또는 문자열 -> 문자열)"""
        return str(id_val)

    def get_next_comment_id(self) -> str:
        """다음 댓글 ID 생성"""
        return str(uuid4())

    def create_comment(self, post_id: Union[UUID, str], user_id: Union[UUID, str], user_nickname: str, content: str) -> Dict:
        """댓글 생성"""
        comment_id = self.get_next_comment_id()
        post_id_str = self._normalize_id(post_id)
        user_id_str = self._normalize_id(user_id)

        comment_data = {
            "comment_id": comment_id,
            "post_id": post_id_str,
            "user_id": user_id_str,
            "user_nickname": user_nickname,
            "content": content,
            "created_at": datetime.now().isoformat(),
            "updated_at": None
        }

        self.comments_db[comment_id] = comment_data
        return comment_data.copy()

    def get_comments_by_post(self, post_id: Union[UUID, str]) -> List[Dict]:
        """특정 게시글의 모든 댓글 조회 (최신순)"""
        post_id_str = self._normalize_id(post_id)
        post_comments = [
            comment for comment in self.comments_db.values()
            if comment["post_id"] == post_id_str
        ]
        # 최신순 정렬
        return sorted(post_comments, key=lambda x: x["created_at"], reverse=True)

    def get_comment_by_id(self, comment_id: Union[UUID, str]) -> Optional[Dict]:
        """ID로 댓글 조회"""
        comment_id_str = self._normalize_id(comment_id)
        return self.comments_db.get(comment_id_str)

    def update_comment(self, comment_id: Union[UUID, str], content: str) -> Optional[Dict]:
        """댓글 수정"""
        comment_id_str = self._normalize_id(comment_id)
        if comment_id_str not in self.comments_db:
            return None

        comment = self.comments_db[comment_id_str]
        comment["content"] = content
        comment["updated_at"] = datetime.now().isoformat()

        return comment.copy()

    def delete_comment(self, comment_id: Union[UUID, str]) -> bool:
        """댓글 삭제"""
        comment_id_str = self._normalize_id(comment_id)
        if comment_id_str in self.comments_db:
            del self.comments_db[comment_id_str]
            return True
        return False

    def get_comments_by_user(self, user_id: Union[UUID, str]) -> List[Dict]:
        """특정 사용자의 모든 댓글 조회"""
        user_id_str = self._normalize_id(user_id)
        return [
            comment for comment in self.comments_db.values()
            if comment["user_id"] == user_id_str
        ]

    def get_comments_count_by_post(self, post_id: Union[UUID, str]) -> int:
        """특정 게시글의 댓글 수 조회"""
        post_id_str = self._normalize_id(post_id)
        return len([
            comment for comment in self.comments_db.values()
            if comment["post_id"] == post_id_str
        ])

    def delete_comments_by_post(self, post_id: Union[UUID, str]) -> int:
        """특정 게시글의 모든 댓글 삭제"""
        post_id_str = self._normalize_id(post_id)
        comments_to_delete = [
            comment_id for comment_id, comment in self.comments_db.items()
            if comment["post_id"] == post_id_str
        ]

        for comment_id in comments_to_delete:
            del self.comments_db[comment_id]

        return len(comments_to_delete)

    def get_total_comments_count(self) -> int:
        """전체 댓글 수 조회"""
        return len(self.comments_db)


# Model 인스턴스 생성
comment_model = CommentModel()

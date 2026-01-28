from typing import Dict, List, Optional, Union
from utils.common.id_utils import generate_id
from utils.database.db import fetch_one, fetch_all, execute


class PostModel:
    """게시글 데이터 관리 Model"""

    def _normalizeId(self, idVal: Union[str, any]) -> str:
        """ID 정규화 (문자열로 변환)"""
        return str(idVal)

    def _format_datetime(self, value) -> Optional[str]:
        if not value:
            return None
        return value.isoformat()

    def _row_to_post(self, row: Optional[Dict]) -> Optional[Dict]:
        if not row:
            return None
        return {
            "postId": row["post_id"],
            "title": row["title"],
            "content": row["content"],
            "authorId": row["author_id"],
            "authorNickname": row.get("author_nickname"),
            "fileUrl": row.get("post_image_url"),
            "createdAt": self._format_datetime(row.get("created_at")),
            "updatedAt": self._format_datetime(row.get("updated_at")),
            "hits": row.get("hits", 0),
            "likeCount": row.get("like_count", 0),
            "commentCount": row.get("comment_count", 0),
        }

    def clear(self):
        """저장소 초기화 (테스트용)"""
        execute("DELETE FROM post_likes")
        execute("DELETE FROM posts")

    def getNextPostId(self) -> str:
        """다음 게시글 ID 생성 (ULID)"""
        return generate_id()

    def createPost(
        self,
        title: str,
        content: str,
        authorId: Union[str, any],
        authorNickname: str,
        fileUrl: Optional[str] = None,
    ) -> Dict:
        """게시글 생성"""
        postId = self.getNextPostId()
        authorIdStr = self._normalizeId(authorId)

        execute(
            """
            INSERT INTO posts (post_id, user_id, title, content, post_image_url, hits, comment_count, created_at)
            VALUES (%s, %s, %s, %s, %s, 0, 0, NOW())
            """,
            (postId, authorIdStr, title, content, fileUrl),
        )

        post = self.getPostById(postId)
        if post:
            post["authorNickname"] = authorNickname
        return post

    def getPosts(self, limit: int = 10, offset: int = 0) -> Dict[str, Union[List[Dict], int]]:
        """게시글 목록 조회 (페이징 지원)"""
        rows = fetch_all(
            """
            SELECT
                p.post_id,
                p.user_id AS author_id,
                u.nickname AS author_nickname,
                p.title,
                p.content,
                p.post_image_url,
                p.created_at,
                p.updated_at,
                p.hits,
                p.comment_count,
                (SELECT COUNT(*) FROM post_likes pl WHERE pl.post_id = p.post_id) AS like_count
            FROM posts p
            LEFT JOIN users u ON u.user_id = p.user_id
            WHERE p.deleted_at IS NULL
            ORDER BY p.created_at DESC
            LIMIT %s OFFSET %s
            """,
            (limit, offset),
        )

        total_row = fetch_one("SELECT COUNT(*) AS total FROM posts WHERE deleted_at IS NULL")
        totalCount = total_row["total"] if total_row else 0

        return {
            "posts": [self._row_to_post(row) for row in rows],
            "totalCount": totalCount,
        }

    def getPostById(self, postId: Union[str, any]) -> Optional[Dict]:
        """게시글 ID로 조회"""
        postIdStr = self._normalizeId(postId)
        row = fetch_one(
            """
            SELECT
                p.post_id,
                p.user_id AS author_id,
                u.nickname AS author_nickname,
                p.title,
                p.content,
                p.post_image_url,
                p.created_at,
                p.updated_at,
                p.hits,
                p.comment_count,
                (SELECT COUNT(*) FROM post_likes pl WHERE pl.post_id = p.post_id) AS like_count
            FROM posts p
            LEFT JOIN users u ON u.user_id = p.user_id
            WHERE p.post_id = %s AND p.deleted_at IS NULL
            """,
            (postIdStr,),
        )
        return self._row_to_post(row)

    def incrementViewCount(self, postId: Union[str, any]) -> bool:
        """조회수 증가"""
        postIdStr = self._normalizeId(postId)
        affected = execute(
            "UPDATE posts SET hits = hits + 1 WHERE post_id = %s AND deleted_at IS NULL",
            (postIdStr,),
        )
        return affected > 0

    def updatePost(
        self,
        postId: Union[str, any],
        title: str,
        content: str,
        fileUrl: Optional[str] = None,
    ) -> Optional[Dict]:
        """게시글 수정"""
        postIdStr = self._normalizeId(postId)
        fields = ["title = %s", "content = %s", "updated_at = NOW()"]
        params = [title, content]

        if fileUrl is not None:
            fields.append("post_image_url = %s")
            params.append(fileUrl)

        params.append(postIdStr)
        execute(
            f"""
            UPDATE posts
            SET {', '.join(fields)}
            WHERE post_id = %s AND deleted_at IS NULL
            """,
            params,
        )
        return self.getPostById(postIdStr)

    def deletePost(self, postId: Union[str, any]) -> bool:
        """게시글 삭제"""
        postIdStr = self._normalizeId(postId)
        affected = execute(
            "UPDATE posts SET deleted_at = NOW() WHERE post_id = %s AND deleted_at IS NULL",
            (postIdStr,),
        )
        return affected > 0

    def getTotalPostsCount(self) -> int:
        """전체 게시글 수 조회"""
        row = fetch_one("SELECT COUNT(*) AS total FROM posts WHERE deleted_at IS NULL")
        return row["total"] if row else 0

    def toggleLike(self, postId: Union[str, any], userId: Union[str, any]) -> int:
        """좋아요 토글"""
        postIdStr = self._normalizeId(postId)
        userIdStr = self._normalizeId(userId)

        existing = fetch_one(
            "SELECT 1 FROM post_likes WHERE post_id = %s AND user_id = %s",
            (postIdStr, userIdStr),
        )

        if existing:
            execute(
                "DELETE FROM post_likes WHERE post_id = %s AND user_id = %s",
                (postIdStr, userIdStr),
            )
        else:
            execute(
                "INSERT INTO post_likes (post_id, user_id, created_at) VALUES (%s, %s, NOW())",
                (postIdStr, userIdStr),
            )

        count_row = fetch_one(
            "SELECT COUNT(*) AS cnt FROM post_likes WHERE post_id = %s",
            (postIdStr,),
        )
        return count_row["cnt"] if count_row else 0

    def updateCommentCount(self, postId: Union[str, any], delta: int) -> int:
        """댓글 수 업데이트 (캐시)"""
        postIdStr = self._normalizeId(postId)
        execute(
            "UPDATE posts SET comment_count = comment_count + %s WHERE post_id = %s AND deleted_at IS NULL",
            (delta, postIdStr),
        )
        row = fetch_one(
            "SELECT comment_count FROM posts WHERE post_id = %s AND deleted_at IS NULL",
            (postIdStr,),
        )
        return row["comment_count"] if row else 0

    def updateAuthorNickname(self, authorId: str, newNickname: str) -> int:
        """작성자 닉네임 일괄 업데이트 (DB 정규화로 인해 no-op)"""
        return 0

    def getLikeCount(self, postId: Union[str, any]) -> int:
        """좋아요 수 조회"""
        postIdStr = self._normalizeId(postId)
        row = fetch_one(
            "SELECT COUNT(*) AS cnt FROM post_likes WHERE post_id = %s",
            (postIdStr,),
        )
        return row["cnt"] if row else 0

    def isLikedByUser(self, postId: Union[str, any], userId: Union[str, any]) -> bool:
        """특정 사용자의 좋아요 여부"""
        postIdStr = self._normalizeId(postId)
        userIdStr = self._normalizeId(userId)
        row = fetch_one(
            "SELECT 1 FROM post_likes WHERE post_id = %s AND user_id = %s",
            (postIdStr, userIdStr),
        )
        return row is not None


# Model 인스턴스 생성
post_model = PostModel()

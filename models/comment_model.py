from typing import Dict, List, Optional, Union
from datetime import datetime
from uuid import UUID, uuid4


class CommentModel:
    """댓글 데이터 관리 Model"""

    def __init__(self):
        # 메모리 기반 댓글 저장소 (Key를 문자열로 관리)
        self.commentsDb: Dict[str, Dict] = {}

    def _normalizeId(self, idVal: Union[UUID, str]) -> str:
        """ID 정규화 (UUID 객체 또는 문자열 -> 문자열)"""
        return str(idVal)

    def getNextCommentId(self) -> str:
        """다음 댓글 ID 생성"""
        return str(uuid4())

    def createComment(self, postId: Union[UUID, str], userId: Union[UUID, str], userNickname: str, content: str) -> Dict:
        """댓글 생성"""
        commentId = self.getNextCommentId()
        postIdStr = self._normalizeId(postId)
        userIdStr = self._normalizeId(userId)

        commentData = {
            "commentId": commentId,
            "postId": postIdStr,
            "userId": userIdStr,
            "userNickname": userNickname,
            "content": content,
            "createdAt": datetime.now().isoformat(),
            "updatedAt": None
        }

        self.commentsDb[commentId] = commentData
        return commentData.copy()

    def getCommentsByPost(self, postId: Union[UUID, str]) -> List[Dict]:
        """특정 게시글의 모든 댓글 조회 (최신순)"""
        postIdStr = self._normalizeId(postId)
        postComments = [
            comment for comment in self.commentsDb.values()
            if comment["postId"] == postIdStr
        ]
        # 최신순 정렬
        return sorted(postComments, key=lambda x: x["createdAt"], reverse=True)

    def getCommentById(self, commentId: Union[UUID, str]) -> Optional[Dict]:
        """ID로 댓글 조회"""
        commentIdStr = self._normalizeId(commentId)
        return self.commentsDb.get(commentIdStr)

    def updateComment(self, commentId: Union[UUID, str], content: str) -> Optional[Dict]:
        """댓글 수정"""
        commentIdStr = self._normalizeId(commentId)
        if commentIdStr not in self.commentsDb:
            return None

        comment = self.commentsDb[commentIdStr]
        comment["content"] = content
        comment["updatedAt"] = datetime.now().isoformat()

        return comment.copy()

    def deleteComment(self, commentId: Union[UUID, str]) -> bool:
        """댓글 삭제"""
        commentIdStr = self._normalizeId(commentId)
        if commentIdStr in self.commentsDb:
            del self.commentsDb[commentIdStr]
            return True
        return False

    def getCommentsByUser(self, userId: Union[UUID, str]) -> List[Dict]:
        """특정 사용자의 모든 댓글 조회"""
        userIdStr = self._normalizeId(userId)
        return [
            comment for comment in self.commentsDb.values()
            if comment["userId"] == userIdStr
        ]

    def getCommentsCountByPost(self, postId: Union[UUID, str]) -> int:
        """특정 게시글의 댓글 수 조회"""
        postIdStr = self._normalizeId(postId)
        return len([
            comment for comment in self.commentsDb.values()
            if comment["postId"] == postIdStr
        ])

    def deleteCommentsByPost(self, postId: Union[UUID, str]) -> int:
        """특정 게시글의 모든 댓글 삭제"""
        postIdStr = self._normalizeId(postId)
        commentsToDelete = [
            commentId for commentId, comment in self.commentsDb.items()
            if comment["postId"] == postIdStr
        ]

        for commentId in commentsToDelete:
            del self.commentsDb[commentId]

        return len(commentsToDelete)

    def getTotalCommentsCount(self) -> int:
        """전체 댓글 수 조회"""
        return len(self.commentsDb)


# Model 인스턴스 생성
comment_model = CommentModel()

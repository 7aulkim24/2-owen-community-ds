from typing import Dict, List, Optional, Union
from datetime import datetime
from utils.id_utils import generate_id


class CommentModel:
    """댓글 데이터 관리 Model"""

    def __init__(self):
        # 메모리 기반 댓글 저장소 (Key를 문자열로 관리)
        self.commentsDb: Dict[str, Dict] = {}

    def _normalizeId(self, idVal: Union[str, any]) -> str:
        """ID 정규화 (문자열로 변환)"""
        return str(idVal)

    def clear(self):
        """저장소 초기화 (테스트용)"""
        self.commentsDb.clear()

    def getNextCommentId(self) -> str:
        """다음 댓글 ID 생성 (ULID)"""
        return generate_id()

    def createComment(self, postId: Union[str, any], userId: Union[str, any], userNickname: str, content: str) -> Dict:
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

    def getCommentsByPost(self, postId: Union[str, any]) -> List[Dict]:
        """특정 게시글의 모든 댓글 조회 (최신순)"""
        postIdStr = self._normalizeId(postId)
        postComments = [
            comment for comment in self.commentsDb.values()
            if comment["postId"] == postIdStr
        ]
        # 최신순 정렬
        return sorted(postComments, key=lambda x: x["createdAt"], reverse=True)

    def getCommentById(self, commentId: Union[str, any]) -> Optional[Dict]:
        """ID로 댓글 조회"""
        commentIdStr = self._normalizeId(commentId)
        return self.commentsDb.get(commentIdStr)

    def updateComment(self, commentId: Union[str, any], content: str) -> Optional[Dict]:
        """댓글 수정"""
        commentIdStr = self._normalizeId(commentId)
        if commentIdStr not in self.commentsDb:
            return None

        comment = self.commentsDb[commentIdStr]
        comment["content"] = content
        comment["updatedAt"] = datetime.now().isoformat()

        return comment.copy()

    def deleteComment(self, commentId: Union[str, any]) -> bool:
        """댓글 삭제"""
        commentIdStr = self._normalizeId(commentId)
        if commentIdStr in self.commentsDb:
            del self.commentsDb[commentIdStr]
            return True
        return False

    def getCommentsByUser(self, userId: Union[str, any]) -> List[Dict]:
        """특정 사용자의 모든 댓글 조회"""
        userIdStr = self._normalizeId(userId)
        return [
            comment for comment in self.commentsDb.values()
            if comment["userId"] == userIdStr
        ]

    def getCommentsCountByPost(self, postId: Union[str, any]) -> int:
        """특정 게시글의 댓글 수 조회"""
        postIdStr = self._normalizeId(postId)
        return len([
            comment for comment in self.commentsDb.values()
            if comment["postId"] == postIdStr
        ])

    def deleteCommentsByPost(self, postId: Union[str, any]) -> int:
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

    def updateUserNickname(self, userId: str, newNickname: str) -> int:
        """사용자 닉네임 일괄 업데이트"""
        count = 0
        for comment in self.commentsDb.values():
            if comment["userId"] == userId:
                comment["userNickname"] = newNickname
                count += 1
        return count


# Model 인스턴스 생성
comment_model = CommentModel()

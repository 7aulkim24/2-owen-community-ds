from typing import Dict, List, Optional, Union
from datetime import datetime
from utils.id_utils import generate_id


class PostModel:
    """게시글 데이터 관리 Model"""

    def __init__(self):
        # 메모리 기반 게시글 저장소 (Key를 문자열로 관리하여 JSON 직렬화 호환성 확보)
        self.postsDb: Dict[str, Dict] = {}
        # 좋아요 기록 저장소 {postId: {userId1, userId2, ...}}
        self.likesDb: Dict[str, set] = {}

    def _normalizeId(self, idVal: Union[str, any]) -> str:
        """ID 정규화 (문자열로 변환)"""
        return str(idVal)

    def clear(self):
        """저장소 초기화 (테스트용)"""
        self.postsDb.clear()
        self.likesDb.clear()

    def getNextPostId(self) -> str:
        """다음 게시글 ID 생성 (ULID)"""
        return generate_id()

    def createPost(self, title: str, content: str, authorId: Union[str, any], authorNickname: str, fileUrl: Optional[str] = None) -> Dict:
        """게시글 생성"""
        postId = self.getNextPostId()
        authorIdStr = self._normalizeId(authorId)

        postData = {
            "postId": postId,
            "title": title,
            "content": content,
            "authorId": authorIdStr,
            "authorNickname": authorNickname,
            "fileUrl": fileUrl,
            "createdAt": datetime.now().isoformat(),
            "updatedAt": None,
            "hits": 0,
            "likeCount": 0,
            "commentCount": 0
        }

        self.postsDb[postId] = postData
        self.likesDb[postId] = set()
        return postData.copy()

    def getPosts(self, limit: int = 10, offset: int = 0) -> Dict[str, Union[List[Dict], int]]:
        """게시글 목록 조회 (페이징 지원)"""
        # 최신순 정렬
        postsList = sorted(
            self.postsDb.values(),
            key=lambda x: x["createdAt"],
            reverse=True
        )

        totalCount = len(postsList)

        # 페이징 적용
        startIdx = offset
        endIdx = offset + limit
        return {
            "posts": postsList[startIdx:endIdx],
            "totalCount": totalCount
        }

    def getPostById(self, postId: Union[str, any]) -> Optional[Dict]:
        """게시글 ID로 조회"""
        postIdStr = self._normalizeId(postId)
        return self.postsDb.get(postIdStr)

    def incrementViewCount(self, postId: Union[str, any]) -> bool:
        """조회수 증가"""
        postIdStr = self._normalizeId(postId)
        if postIdStr in self.postsDb:
            self.postsDb[postIdStr]["hits"] += 1
            return True
        return False

    def updatePost(self, postId: Union[str, any], title: str, content: str, fileUrl: Optional[str] = None) -> Optional[Dict]:
        """게시글 수정"""
        postIdStr = self._normalizeId(postId)
        if postIdStr not in self.postsDb:
            return None

        post = self.postsDb[postIdStr]
        post["title"] = title
        post["content"] = content
        if fileUrl is not None:
            post["fileUrl"] = fileUrl
        post["updatedAt"] = datetime.now().isoformat()

        return post.copy()

    def deletePost(self, postId: Union[str, any]) -> bool:
        """게시글 삭제"""
        postIdStr = self._normalizeId(postId)
        if postIdStr in self.postsDb:
            del self.postsDb[postIdStr]
            if postIdStr in self.likesDb:
                del self.likesDb[postIdStr]
            return True
        return False

    def getTotalPostsCount(self) -> int:
        """전체 게시글 수 조회"""
        return len(self.postsDb)

    def toggleLike(self, postId: Union[str, any], userId: Union[str, any]) -> int:
        """좋아요 토글"""
        postIdStr = self._normalizeId(postId)
        userIdStr = self._normalizeId(userId)
        
        if postIdStr not in self.likesDb:
            self.likesDb[postIdStr] = set()
            
        if userIdStr in self.likesDb[postIdStr]:
            self.likesDb[postIdStr].remove(userIdStr)
        else:
            self.likesDb[postIdStr].add(userIdStr)
            
        # 캐시된 카운트 업데이트
        count = len(self.likesDb[postIdStr])
        if postIdStr in self.postsDb:
            self.postsDb[postIdStr]["likeCount"] = count
            
        return count

    def updateCommentCount(self, postId: Union[str, any], delta: int) -> int:
        """댓글 수 업데이트 (캐시)"""
        postIdStr = self._normalizeId(postId)
        if postIdStr in self.postsDb:
            self.postsDb[postIdStr]["commentCount"] += delta
            return self.postsDb[postIdStr]["commentCount"]
        return 0

    def updateAuthorNickname(self, authorId: str, newNickname: str) -> int:
        """작성자 닉네임 일괄 업데이트"""
        count = 0
        for post in self.postsDb.values():
            if post["authorId"] == authorId:
                post["authorNickname"] = newNickname
                count += 1
        return count

    def getLikeCount(self, postId: Union[str, any]) -> int:
        """좋아요 수 조회"""
        postIdStr = self._normalizeId(postId)
        return len(self.likesDb.get(postIdStr, set()))

    def isLikedByUser(self, postId: Union[str, any], userId: Union[str, any]) -> bool:
        """특정 사용자의 좋아요 여부"""
        postIdStr = self._normalizeId(postId)
        userIdStr = self._normalizeId(userId)
        return userIdStr in self.likesDb.get(postIdStr, set())


# Model 인스턴스 생성
post_model = PostModel()

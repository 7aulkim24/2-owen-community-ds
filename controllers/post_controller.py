from typing import List, Dict, Union, Optional
from models.post_model import post_model
from models.comment_model import comment_model
from models.user_model import user_model
from utils.exceptions import APIError
from utils.error_codes import ErrorCode
from schemas import PostCreateRequest, PostUpdateRequest, PostResponse, PostAuthor, PostFile, PaginatedData, PaginationMeta, ResourceError


class PostController:
    """게시글 관련 비즈니스 로직"""

    def _formatPost(self, post: Dict, user_cache: Optional[Dict[str, Dict]] = None) -> PostResponse:
        """Post 데이터를 API 응답 규격에 맞게 변환"""
        author_id = post["authorId"]
        
        # 캐시가 제공되면 캐시에서 조회, 없으면 모델에서 직접 조회
        if user_cache is not None and author_id in user_cache:
            author = user_cache[author_id]
        else:
            author = user_model.getUserById(author_id)
        
        # author 정보가 있으면 (탈퇴 등) 최신 닉네임 사용, 없으면 post에 저장된 값 사용
        nickname = author.get("nickname") if author else post["authorNickname"]
        
        author_data = PostAuthor(
            userId=author_id,
            nickname=nickname,
            profileImageUrl=author.get("profileImageUrl") if author else None
        )

        post_file = None
        if post.get("fileUrl"):
            post_file = PostFile(
                fileId=post["postId"], # 임시로 postId 사용
                fileUrl=post["fileUrl"]
            )

        return PostResponse(
            postId=post["postId"],
            title=post["title"],
            content=post["content"],
            likeCount=post.get("likeCount", 0), # 캐시된 값 사용
            commentCount=post.get("commentCount", 0), # 캐시된 값 사용
            hits=post["hits"],
            author=author_data,
            file=post_file,
            createdAt=post["createdAt"],
            updatedAt=post.get("updatedAt"),
        )

    def getAllPosts(self, limit: int = 10, offset: int = 0) -> PaginatedData[List[PostResponse]]:
        """게시글 목록 조회 로직 (페이징 메타데이터 포함)"""
        result = post_model.getPosts(limit=limit, offset=offset)
        posts_data = result["posts"]
        total_count = result["totalCount"]

        # 중복 사용자 조회 최적화를 위한 캐싱
        author_ids = {post["authorId"] for post in posts_data}
        user_cache = {}
        for aid in author_ids:
            user_cache[aid] = user_model.getUserById(aid)

        formatted_posts = [self._formatPost(post, user_cache) for post in posts_data]
        
        # 페이징 메타데이터 계산
        total_page = (total_count + limit - 1) // limit if total_count > 0 else 0
        current_page = (offset // limit) + 1
        has_next = offset + limit < total_count

        return PaginatedData(
            items=formatted_posts,
            pagination=PaginationMeta(
                totalCount=total_count,
                limit=limit,
                offset=offset,
                currentPage=current_page,
                totalPage=total_page,
                hasNext=has_next
            )
        )

    def getPostById(self, postId: str, incHits: bool = True) -> PostResponse:
        """게시글 상세 조회 로직"""
        post = post_model.getPostById(postId)
        if not post:
            raise APIError(
                ErrorCode.POST_NOT_FOUND, 
                ResourceError(resource="게시글", id=postId)
            )

        # 조회수 증가 (필요한 경우만)
        if incHits:
            post_model.incrementViewCount(postId)
            # 증가된 데이터 반영을 위해 다시 조회
            post = post_model.getPostById(postId)

        return self._formatPost(post)

    def createPost(self, req: PostCreateRequest, user: Dict) -> PostResponse:
        """게시글 생성 로직"""
        post_data = post_model.createPost(
            title=req.title,
            content=req.content,
            authorId=user["userId"],
            authorNickname=user["nickname"],
            fileUrl=req.fileUrl
        )

        return self._formatPost(post_data)

    def updatePost(self, postId: str, req: PostUpdateRequest, user: Dict) -> PostResponse:
        """게시글 수정 로직"""
        post = post_model.getPostById(postId)
        if not post:
            raise APIError(
                ErrorCode.POST_NOT_FOUND, 
                ResourceError(resource="게시글", id=postId)
            )

        # 권한 확인 (작성자 확인)
        if str(post["authorId"]) != str(user["userId"]):
            raise APIError(ErrorCode.FORBIDDEN, ResourceError(resource="게시글"))

        updated_post = post_model.updatePost(
            postId=postId,
            title=req.title,
            content=req.content,
            fileUrl=req.fileUrl
        )

        return self._formatPost(updated_post)

    def deletePost(self, postId: str, user: Dict) -> Dict:
        """게시글 삭제 로직"""
        post = post_model.getPostById(postId)
        if not post:
            raise APIError(
                ErrorCode.POST_NOT_FOUND, 
                ResourceError(resource="게시글", id=postId)
            )

        # 권한 확인
        if str(post["authorId"]) != str(user["userId"]):
            raise APIError(ErrorCode.FORBIDDEN, ResourceError(resource="게시글"))

        # 게시글 삭제 시 관련 댓글들도 함께 삭제
        comment_model.deleteCommentsByPost(postId)

        # Model을 통해 게시글 삭제
        post_model.deletePost(postId)

        return post

    def togglePostLike(self, postId: str, userId: str) -> Dict:
        """게시글 좋아요 토글"""
        post = post_model.getPostById(postId)
        if not post:
            raise APIError(ErrorCode.POST_NOT_FOUND, ResourceError(resource="게시글", id=postId))
            
        likeCount = post_model.toggleLike(postId, userId)
        return {"likeCount": likeCount}


post_controller = PostController()

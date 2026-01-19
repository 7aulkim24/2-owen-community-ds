from typing import List, Dict, Union, Optional
from uuid import UUID
from models import post_model, comment_model, user_model
from utils.exceptions import APIError
from utils.error_codes import ErrorCode
from schemas.post_schema import PostCreateRequest, PostUpdateRequest
from schemas.error_schema import ResourceError


class PostController:
    """게시글 관련 비즈니스 로직"""

    def _formatPost(self, post: Dict) -> Dict:
        """Post 데이터를 API 응답 규격에 맞게 변환"""
        author = user_model.getUserById(post["authorId"])
        
        # author 정보가 없으면 (탈퇴 등) 기본값 처리
        authorData = {
            "userId": post["authorId"],
            "nickname": post["authorNickname"],
            "profileImageUrl": author.get("profileImageUrl") if author else None
        }

        formatted = {
            "postId": post["postId"],
            "title": post["title"],
            "content": post["content"],
            "likeCount": post_model.getLikeCount(post["postId"]),
            "commentCount": comment_model.getCommentsCountByPost(post["postId"]),
            "hits": post["hits"],
            "author": authorData,
            "createdAt": post["createdAt"],
            "updatedAt": post.get("updatedAt"),
        }
        
        if post.get("fileUrl"):
            formatted["file"] = {
                "fileId": post["postId"], # 임시로 postId 사용
                "fileUrl": post["fileUrl"]
            }
        else:
            formatted["file"] = None
            
        return formatted

    def getAllPosts(self, limit: int = 10, offset: int = 0) -> Dict:
        """게시글 목록 조회 로직 (페이징 메타데이터 포함)"""
        result = post_model.getPosts(limit=limit, offset=offset)
        postsData = result["posts"]
        totalCount = result["totalCount"]

        formattedPosts = [self._formatPost(post) for post in postsData]
        
        # 페이징 메타데이터 계산
        totalPage = (totalCount + limit - 1) // limit if totalCount > 0 else 0
        currentPage = (offset // limit) + 1
        hasNext = offset + limit < totalCount

        return {
            "items": formattedPosts,
            "pagination": {
                "totalCount": totalCount,
                "limit": limit,
                "offset": offset,
                "currentPage": currentPage,
                "totalPage": totalPage,
                "hasNext": hasNext
            }
        }

    def getPostById(self, postId: Union[UUID, str]) -> Dict:
        """게시글 상세 조회 로직"""
        post = post_model.getPostById(postId)
        if not post:
            raise APIError(
                ErrorCode.POST_NOT_FOUND, 
                ResourceError(resource="게시글", id=str(postId))
            )

        # 조회수 증가
        post_model.incrementViewCount(postId)
        # 증가된 데이터 반영을 위해 다시 조회
        post = post_model.getPostById(postId)

        return self._formatPost(post)

    def createPost(self, req: PostCreateRequest, user: Dict) -> Dict:
        """게시글 생성 로직"""
        postData = post_model.createPost(
            title=req.title,
            content=req.content,
            authorId=user["userId"],
            authorNickname=user["nickname"],
            fileUrl=req.fileUrl
        )

        return self._formatPost(postData)

    def updatePost(self, postId: Union[UUID, str], req: PostUpdateRequest, user: Dict) -> Dict:
        """게시글 수정 로직"""
        post = post_model.getPostById(postId)
        if not post:
            raise APIError(
                ErrorCode.POST_NOT_FOUND, 
                ResourceError(resource="게시글", id=str(postId))
            )

        # 권한 확인 (작성자 확인)
        if str(post["authorId"]) != str(user["userId"]):
            raise APIError(ErrorCode.FORBIDDEN, ResourceError(resource="게시글"))

        updatedPost = post_model.updatePost(
            postId=postId,
            title=req.title,
            content=req.content,
            fileUrl=req.fileUrl
        )

        return self._formatPost(updatedPost)

    def deletePost(self, postId: Union[UUID, str], user: Dict) -> Dict:
        """게시글 삭제 로직"""
        post = post_model.getPostById(postId)
        if not post:
            raise APIError(
                ErrorCode.POST_NOT_FOUND, 
                ResourceError(resource="게시글", id=str(postId))
            )

        # 권한 확인
        if str(post["authorId"]) != str(user["userId"]):
            raise APIError(ErrorCode.FORBIDDEN, ResourceError(resource="게시글"))

        # 게시글 삭제 시 관련 댓글들도 함께 삭제
        comment_model.deleteCommentsByPost(postId)

        # Model을 통해 게시글 삭제
        post_model.deletePost(postId)

        return post

    def togglePostLike(self, postId: Union[UUID, str], userId: Union[UUID, str]) -> Dict:
        """게시글 좋아요 토글"""
        post = post_model.getPostById(postId)
        if not post:
            raise APIError(ErrorCode.POST_NOT_FOUND, ResourceError(resource="게시글", id=str(postId)))
            
        likeCount = post_model.toggleLike(postId, userId)
        return {"likeCount": likeCount}


post_controller = PostController()

from fastapi import APIRouter, status
from models.post import PostRequest
from utils.response import StandardResponse
from controllers.post_controller import post_controller

router = APIRouter(prefix="/v1/posts", tags=["게시글"])

@router.get("", response_model=None, status_code=status.HTTP_200_OK)
async def get_posts():
    """
    게시글 목록 조회
    - 모든 게시글을 최신순으로 반환
    - 인증 불필요
    """
    data = post_controller.get_all_posts()
    return StandardResponse.success("GET_POSTS_SUCCESS", data)

@router.get("/{post_id}", response_model=None, status_code=status.HTTP_200_OK)
async def get_post(post_id: int):
    """
    게시글 상세 조회
    - 특정 게시글의 상세 정보 반환
    - 인증 불필요
    """
    data = post_controller.get_post_by_id(post_id)
    return StandardResponse.success("GET_POST_SUCCESS", data)

@router.post("", response_model=None, status_code=status.HTTP_201_CREATED)
async def create_post(req: PostRequest):
    """
    게시글 생성
    - 인증된 사용자만 작성 가능 (Phase 2에서는 Mock 사용)
    - title, content 필수
    """
    data = post_controller.create_post(req)
    return StandardResponse.success("CREATE_POST_SUCCESS", data, 201)

@router.patch("/{post_id}", response_model=None, status_code=status.HTTP_200_OK)
async def update_post(post_id: int, req: PostRequest):
    """
    게시글 수정
    - 작성자만 수정 가능 (Phase 2에서는 Mock 사용)
    - title, content 수정 가능
    """
    data = post_controller.update_post(post_id, req)
    return StandardResponse.success("UPDATE_POST_SUCCESS", data)

@router.delete("/{post_id}", response_model=None, status_code=status.HTTP_200_OK)
async def delete_post(post_id: int):
    """
    게시글 삭제
    - 작성자만 삭제 가능 (Phase 2에서는 Mock 사용)
    """
    deleted_post = post_controller.delete_post(post_id)
    return StandardResponse.success(
        "DELETE_POST_SUCCESS", 
        {"post_id": deleted_post["post_id"], "message": "게시글이 삭제되었습니다"}
    )

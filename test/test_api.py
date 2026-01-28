import pytest
import os
import sys

# 프로젝트 루트를 path에 추가하여 utils, models 등을 가져올 수 있게 함
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../2-owen-community-be"))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from utils.common.id_utils import generate_id
from models.user_model import user_model
from models.post_model import post_model
from models.comment_model import comment_model
from utils.test.test_utils import seed_database

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # 데이터베이스 초기화
    seed_database()
    yield

# --- Auth API Tests ---

def test_signup_success(api_client):
    """회원가입 성공 케이스"""
    response = api_client.post("/v1/auth/signup", json={
        "email": "test@example.com", 
        "password": "password123", 
        "nickname": "tester"
    })
    assert response.status_code == 201
    assert response.json()["code"] == "CREATED"
    assert response.json()["data"]["email"] == "test@example.com"

def test_signup_failure_invalid_input(api_client):
    """회원가입 실패: 유효하지 않은 입력"""
    response = api_client.post("/v1/auth/signup", json={
        "email": "invalid-email", 
        "password": "short", 
        "nickname": ""
    })
    assert response.status_code == 422
    assert response.json()["code"] == "INVALID_INPUT"
    details = response.json()["details"]
    assert "email" in details
    assert "password" in details
    assert "nickname" in details

def test_signup_failure_duplicate(api_client):
    """회원가입 실패: 이메일 또는 닉네임 중복"""
    api_client.post("/v1/auth/signup", json={
        "email": "dup@example.com", 
        "password": "password123", 
        "nickname": "user1"
    })
    
    # 이메일 중복
    response = api_client.post("/v1/auth/signup", json={
        "email": "dup@example.com", 
        "password": "password123", 
        "nickname": "user2"
    })
    assert response.status_code == 409
    assert response.json()["code"] == "ALREADY_EXISTS"
    assert response.json()["details"]["field"] == "email"
    
    # 닉네임 중복
    response = api_client.post("/v1/auth/signup", json={
        "email": "other@example.com", 
        "password": "password123", 
        "nickname": "user1"
    })
    assert response.status_code == 409
    assert response.json()["code"] == "ALREADY_EXISTS"
    assert response.json()["details"]["field"] == "nickname"

def test_login_lifecycle(api_client):
    """로그인, 내 정보 조회, 로그아웃 라이프사이클"""
    api_client.post("/v1/auth/signup", json={
        "email": "login@example.com", 
        "password": "password123", 
        "nickname": "tester"
    })
    
    # 로그인 성공
    resp = api_client.post("/v1/auth/login", json={
        "email": "login@example.com", 
        "password": "password123"
    })
    assert resp.status_code == 200
    assert resp.json()["data"]["nickname"] == "tester"
    
    # 내 정보 조회 성공
    resp = api_client.get("/v1/auth/me")
    assert resp.status_code == 200
    assert resp.json()["data"]["email"] == "login@example.com"
    
    # 로그아웃
    resp = api_client.post("/v1/auth/logout")
    assert resp.status_code == 200
    
    # 로그아웃 후 내 정보 조회 실패
    resp = api_client.get("/v1/auth/me")
    assert resp.status_code == 401

def test_login_failure(api_client):
    """로그인 실패 케이스"""
    api_client.post("/v1/auth/signup", json={
        "email": "fail@example.com", 
        "password": "password123", 
        "nickname": "tester"
    })
    
    # 잘못된 비밀번호
    resp = api_client.post("/v1/auth/login", json={
        "email": "fail@example.com", 
        "password": "wrongpassword"
    })
    assert resp.status_code == 401
    assert resp.json()["code"] == "INVALID_CREDENTIALS"
    
    # 존재하지 않는 이메일
    resp = api_client.post("/v1/auth/login", json={
        "email": "none@example.com", 
        "password": "password123"
    })
    assert resp.status_code == 401

# --- User API Tests ---

def test_user_update_success(api_client):
    """사용자 정보 수정 및 비밀번호 변경 성공"""
    signup_resp = api_client.post("/v1/auth/signup", json={
        "email": "update@test.com", 
        "password": "password123", 
        "nickname": "oldNick"
    })
    api_client.post("/v1/auth/login", json={
        "email": "update@test.com", 
        "password": "password123"
    })
    
    # 닉네임 수정
    resp = api_client.patch("/v1/users/me", json={"nickname": "newNick"})
    assert resp.status_code == 200
    assert resp.json()["data"]["nickname"] == "newNick"
    
    # 비밀번호 변경
    resp = api_client.patch("/v1/users/password", json={"password": "newpassword123"})
    assert resp.status_code == 200
    
    # 새 비밀번호로 로그인 확인
    api_client.post("/v1/auth/logout")
    resp = api_client.post("/v1/auth/login", json={
        "email": "update@test.com", 
        "password": "newpassword123"
    })
    assert resp.status_code == 200

def test_user_delete_success(api_client):
    """회원 탈퇴 성공"""
    api_client.post("/v1/auth/signup", json={
        "email": "del@test.com", 
        "password": "password123", 
        "nickname": "to_be_deleted"
    })
    api_client.post("/v1/auth/login", json={
        "email": "del@test.com", 
        "password": "password123"
    })
    
    # 탈퇴
    resp = api_client.delete("/v1/users/me")
    assert resp.status_code == 200
    
    # 탈퇴 후 로그인 불가 확인
    resp = api_client.post("/v1/auth/login", json={
        "email": "del@test.com", 
        "password": "password123"
    })
    assert resp.status_code == 401

# --- Post API Tests ---

def test_post_full_lifecycle(api_client):
    """게시글 생성, 조회, 수정, 좋아요, 삭제 전체 흐름"""
    api_client.post("/v1/auth/signup", json={"email": "p@t.com", "password": "password123", "nickname": "writer"})
    api_client.post("/v1/auth/login", json={"email": "p@t.com", "password": "password123"})
    
    # 1. 생성
    resp = api_client.post("/v1/posts", json={"title": "Test Title", "content": "Test Content"})
    assert resp.status_code == 201
    postId = resp.json()["data"]["postId"]
    
    # 2. 상세 조회 및 조회수 증가 확인
    resp = api_client.get(f"/v1/posts/{postId}")
    assert resp.json()["data"]["hits"] == 1
    
    # 3. 좋아요 토글 (캐시된 카운트 확인)
    resp = api_client.post(f"/v1/posts/{postId}/likes")
    assert resp.json()["data"]["likeCount"] == 1
    
    # 다시 토글해서 취소
    resp = api_client.post(f"/v1/posts/{postId}/likes")
    assert resp.json()["data"]["likeCount"] == 0
    
    # 4. 수정
    resp = api_client.patch(f"/v1/posts/{postId}", json={"title": "Updated Title", "content": "Updated Content"})
    assert resp.status_code == 200
    assert resp.json()["data"]["title"] == "Updated Title"
    
    # 5. 권한 없는 수정 시도
    api_client.post("/v1/auth/signup", json={"email": "h@t.com", "password": "password123", "nickname": "hacker"})
    api_client.post("/v1/auth/login", json={"email": "h@t.com", "password": "password123"})
    resp = api_client.patch(f"/v1/posts/{postId}", json={"title": "Hacked", "content": "Hacked Content"})
    assert resp.status_code == 403
    
    # 6. 삭제
    api_client.post("/v1/auth/login", json={"email": "p@t.com", "password": "password123"})
    resp = api_client.delete(f"/v1/posts/{postId}")
    assert resp.status_code == 200
    
    # 삭제 후 조회 실패 확인
    resp = api_client.get(f"/v1/posts/{postId}")
    assert resp.status_code == 404

# --- Comment API Tests ---

def test_comment_lifecycle_and_cache(api_client):
    """댓글 작성, 수정, 삭제 및 게시글 내 캐시 카운트 검증"""
    api_client.post("/v1/auth/signup", json={"email": "c@t.com", "password": "password123", "nickname": "comm"})
    api_client.post("/v1/auth/login", json={"email": "c@t.com", "password": "password123"})
    
    # 게시글 생성
    post_resp = api_client.post("/v1/posts", json={"title": "Post", "content": "Content"})
    postId = post_resp.json()["data"]["postId"]
    
    # 1. 댓글 작성
    resp = api_client.post(f"/v1/posts/{postId}/comments", json={"content": "First Comment"})
    assert resp.status_code == 201
    commentId = resp.json()["data"]["commentId"]
    
    # 게시글 조회 시 commentCount가 1인지 확인 (최적화 기능 검증)
    post_resp = api_client.get(f"/v1/posts/{postId}")
    assert post_resp.json()["data"]["commentCount"] == 1
    
    # 2. 댓글 수정
    resp = api_client.patch(f"/v1/posts/{postId}/comments/{commentId}", json={"content": "Updated Comment"})
    assert resp.status_code == 200
    assert resp.json()["data"]["content"] == "Updated Comment"
    
    # 3. 댓글 삭제
    resp = api_client.delete(f"/v1/posts/{postId}/comments/{commentId}")
    assert resp.status_code == 200
    
    # 게시글 조회 시 commentCount가 0인지 확인
    post_resp = api_client.get(f"/v1/posts/{postId}")
    assert post_resp.json()["data"]["commentCount"] == 0

# --- File Upload Tests ---

def test_image_upload_and_directory_creation(api_client):
    """이미지 업로드 기능 검증"""
    api_client.post("/v1/auth/signup", json={"email": "f@t.com", "password": "password123", "nickname": "file"})
    api_client.post("/v1/auth/login", json={"email": "f@t.com", "password": "password123"})
    
    # 프로필 이미지 업로드
    files = {"profileImage": ("profile.png", b"fake_image_content", "image/png")}
    resp = api_client.post("/v1/users/me/profile-image", files=files)
    assert resp.status_code == 201
    assert "profileImageUrl" in resp.json()["data"]
    
    # 게시글 이미지 업로드
    files = {"postFile": ("post.jpg", b"fake_post_image", "image/jpeg")}
    resp = api_client.post("/v1/posts/image", files=files)
    assert resp.status_code == 201
    assert "postFileUrl" in resp.json()["data"]

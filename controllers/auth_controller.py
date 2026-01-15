from typing import Dict
from fastapi import Request
from models import user_model
from utils.exceptions import (
    DuplicateEmailError,
    DuplicateNicknameError,
    UnauthorizedError,
    UserNotFoundError,
    ValidationError,
)
from utils.error_codes import ErrorCode
from schemas.auth_schema import SignupRequest, LoginRequest
from schemas.error_schema import ValidationErrorDetail


class AuthController:
    """인증 관련 비즈니스 로직"""

    def _sanitize_user(self, user: Dict) -> Dict:
        """응답에서 민감 정보 제거"""
        return {
            "user_id": user.get("user_id"),
            "email": user.get("email"),
            "nickname": user.get("nickname"),
            "profile_image_url": user.get("profile_image_url"),
            "created_at": user.get("created_at"),
            "updated_at": user.get("updated_at"),
        }

    def signup(self, req: SignupRequest) -> Dict:
        """회원가입"""
        # Pydantic에서 이미 검증되었으므로 수동 필드 검증 제거
        
        if user_model.email_exists(req.email):
            raise DuplicateEmailError(req.email)
        if user_model.nickname_exists(req.nickname):
            raise DuplicateNicknameError(req.nickname)

        user = user_model.create_user(req.email, req.password, req.nickname, req.profile_image_url)
        return self._sanitize_user(user)

    def login(self, req: LoginRequest, request: Request) -> Dict:
        """로그인"""
        # Pydantic에서 이미 검증되었으므로 수동 필드 검증 제거

        user = user_model.authenticate_user(req.email, req.password)
        if not user:
            raise UnauthorizedError(ErrorCode.INVALID_CREDENTIALS)

        request.session["user_id"] = user["user_id"]
        request.session["email"] = user["email"]
        request.session["nickname"] = user["nickname"]
        request.session["profile_image_url"] = user.get("profile_image_url")
        return self._sanitize_user(user)

    def logout(self, request: Request) -> Dict:
        """로그아웃"""
        request.session.clear()
        return {}

    def get_me(self, request: Request) -> Dict:
        """내 정보 조회"""
        if not request.state.user:
            raise UnauthorizedError(ErrorCode.UNAUTHORIZED)

        return self._sanitize_user(request.state.user)


auth_controller = AuthController()

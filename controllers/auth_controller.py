from typing import Dict
from fastapi import Request
from models import user_model
from utils.exceptions import APIError
from utils.error_codes import ErrorCode
from schemas.auth_schema import SignupRequest, LoginRequest
from schemas.error_schema import FieldError


class AuthController:
    """인증 관련 비즈니스 로직"""

    def _sanitizeUser(self, user: Dict) -> Dict:
        """응답에서 민감 정보 제거"""
        return {
            "userId": user.get("userId"),
            "email": user.get("email"),
            "nickname": user.get("nickname"),
            "profileImageUrl": user.get("profileImageUrl"),
            "createdAt": user.get("createdAt"),
            "updatedAt": user.get("updatedAt"),
        }

    def signup(self, req: SignupRequest) -> Dict:
        """회원가입"""
        if user_model.emailExists(req.email):
            raise APIError(ErrorCode.EMAIL_ALREADY_EXISTS, FieldError(field="email", value=req.email))
        if user_model.nicknameExists(req.nickname):
            raise APIError(ErrorCode.NICKNAME_ALREADY_EXISTS, FieldError(field="nickname", value=req.nickname))

        user = user_model.createUser(req.email, req.password, req.nickname, req.profileImageUrl)
        return self._sanitizeUser(user)

    def login(self, req: LoginRequest, request: Request) -> Dict:
        """로그인"""
        user = user_model.authenticateUser(req.email, req.password)
        if not user:
            raise APIError(ErrorCode.INVALID_CREDENTIALS)

        request.session["userId"] = user["userId"]
        request.session["email"] = user["email"]
        request.session["nickname"] = user["nickname"]
        request.session["profileImageUrl"] = user.get("profileImageUrl")
        return self._sanitizeUser(user)

    def logout(self, request: Request) -> Dict:
        """로그아웃"""
        request.session.clear()
        return {}

    def getMe(self, request: Request) -> Dict:
        """내 정보 조회"""
        if not hasattr(request.state, "user") or not request.state.user:
            raise APIError(ErrorCode.UNAUTHORIZED)

        return self._sanitizeUser(request.state.user)

    def checkEmailAvailability(self, email: str) -> Dict:
        """이메일 중복 확인"""
        return {"available": not user_model.emailExists(email)}

    def checkNicknameAvailability(self, nickname: str) -> Dict:
        """닉네임 중복 확인"""
        return {"available": not user_model.nicknameExists(nickname)}


auth_controller = AuthController()

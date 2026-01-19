from typing import Dict, Union
from uuid import UUID
from fastapi import Request
from models import user_model
from utils.exceptions import APIError
from utils.error_codes import ErrorCode
from schemas.user_schema import UserUpdateRequest, PasswordChangeRequest
from schemas.error_schema import ResourceError


class UserController:
    """사용자 관련 비즈니스 로직"""

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

    def getUserById(self, userId: Union[UUID, str]) -> Dict:
        """사용자 정보 조회"""
        user = user_model.getUserById(userId)
        if not user:
            raise APIError(ErrorCode.USER_NOT_FOUND, ResourceError(resource="사용자", id=str(userId)))
        return self._sanitizeUser(user)

    def updateUser(self, userId: Union[UUID, str], req: UserUpdateRequest, currentUser: Dict) -> Dict:
        """사용자 정보 수정"""
        # 본인 확인
        if str(userId) != str(currentUser["userId"]):
            raise APIError(ErrorCode.FORBIDDEN)

        # 닉네임 중복 체크 (본인 닉네임과 다를 경우만)
        if req.nickname != currentUser["nickname"] and user_model.nicknameExists(req.nickname):
            raise APIError(ErrorCode.NICKNAME_ALREADY_EXISTS)

        updateData = {
            "nickname": req.nickname,
            "profileImageUrl": req.profileImageUrl
        }
        updatedUser = user_model.updateUser(userId, updateData)
        return self._sanitizeUser(updatedUser)

    def changePassword(self, userId: Union[UUID, str], req: PasswordChangeRequest, currentUser: Dict) -> Dict:
        """비밀번호 변경"""
        if str(userId) != str(currentUser["userId"]):
            raise APIError(ErrorCode.FORBIDDEN)

        user_model.updateUser(userId, {"password": req.password})
        return {}

    def deleteUser(self, userId: Union[UUID, str], currentUser: Dict, request: Request) -> Dict:
        """회원 탈퇴"""
        if str(userId) != str(currentUser["userId"]):
            raise APIError(ErrorCode.FORBIDDEN)

        user_model.deleteUser(userId)
        request.session.clear()
        return {}


user_controller = UserController()

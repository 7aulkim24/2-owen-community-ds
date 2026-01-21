from typing import Dict, Union
from fastapi import Request
from models.user_model import user_model
from utils.exceptions import APIError
from utils.error_codes import ErrorCode
from schemas import UserUpdateRequest, PasswordChangeRequest, UserResponse, ResourceError, FieldError


class UserController:
    """사용자 관련 비즈니스 로직"""

    def getUserById(self, userId: str) -> UserResponse:
        """사용자 정보 조회"""
        user = user_model.getUserById(userId)
        if not user:
            raise APIError(ErrorCode.USER_NOT_FOUND, ResourceError(resource="사용자", id=userId))
        return UserResponse.model_validate(user)

    def updateUser(self, userId: str, req: UserUpdateRequest, currentUser: Dict) -> UserResponse:
        """사용자 정보 수정"""
        # 본인 확인
        if str(userId) != str(currentUser["userId"]):
            raise APIError(ErrorCode.FORBIDDEN)

        # 닉네임 중복 체크 (본인 닉네임과 다를 경우만)
        if req.nickname != currentUser["nickname"] and user_model.nicknameExists(req.nickname):
            raise APIError(ErrorCode.ALREADY_EXISTS, FieldError(field="nickname", value=req.nickname), message="이미 사용 중인 닉네임입니다.")

        updateData = {
            "nickname": req.nickname,
            "profileImageUrl": req.profileImageUrl
        }
        updatedUser = user_model.updateUser(userId, updateData)
        return UserResponse.model_validate(updatedUser)

    def changePassword(self, userId: str, req: PasswordChangeRequest, currentUser: Dict) -> Dict:
        """비밀번호 변경"""
        if str(userId) != str(currentUser["userId"]):
            raise APIError(ErrorCode.FORBIDDEN)

        user_model.updateUser(userId, {"password": req.password})
        return {}

    def deleteUser(self, userId: str, currentUser: Dict, request: Request) -> Dict:
        """회원 탈퇴"""
        if str(userId) != str(currentUser["userId"]):
            raise APIError(ErrorCode.FORBIDDEN)

        user_model.deleteUser(userId)
        request.session.clear()
        return {}


user_controller = UserController()

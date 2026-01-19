from typing import Dict
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from models.user_model import user_model

from utils.exceptions import APIError
from utils.error_codes import ErrorCode

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 1. 세션에서 userId 추출
        userId = request.session.get("userId")
        request.state.user = None
        
        if userId:
            # 2. DB(메모리)에서 최신 사용자 정보 조회
            user = user_model.getUserById(userId)
            if user:
                # 3. request.state에 사용자 객체 저장
                request.state.user = user
            else:
                # 사용자가 없는 경우 세션 클리어
                request.session.clear()
        
        response = await call_next(request)
        return response


def get_current_user(request: Request) -> Dict:
    """요청에 인증된 사용자 반환 (없으면 401)"""
    if not hasattr(request.state, "user") or not request.state.user:
        raise APIError(ErrorCode.UNAUTHORIZED)
    return request.state.user

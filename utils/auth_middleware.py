from typing import Dict

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from models.user_model import user_model
from utils.exceptions import UnauthorizedError
from utils.error_codes import ErrorCode

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # 1. 세션에서 user_id 추출
        user_id = request.session.get("user_id")
        request.state.user = None
        
        if user_id:
            # 2. DB(메모리)에서 최신 사용자 정보 조회
            # user_model 인스턴스가 이미 있으면 그것을 사용
            from models.user_model import user_model as um_instance
            user = um_instance.get_user_by_id(user_id)
            if user:
                # 3. request.state에 사용자 객체 저장
                request.state.user = user
            else:
                # 사용자가 없는 경우 세션 클리어 (보안상 안전)
                request.session.clear()
        
        response = await call_next(request)
        return response


def get_current_user(request: Request) -> Dict:
    """요청에 인증된 사용자 반환 (없으면 401)"""
    if not request.state.user:
        raise UnauthorizedError(ErrorCode.UNAUTHORIZED)
    return request.state.user

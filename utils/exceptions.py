"""
커스텀 예외 클래스 정의
- APIError 단일 클래스 통합
- ErrorCode 중심의 선언적 구조
- 에러 메시지 FE 위임
"""

from typing import Union, Optional
from pydantic import BaseModel
from .error_codes import ErrorCode, get_error_status


class APIError(Exception):
    """모든 API 에러를 처리하는 단일 예외 클래스"""
    def __init__(
        self, 
        code: ErrorCode, 
        details: Union[BaseModel, dict, None] = None,
        status_code: Optional[int] = None
    ):
        """
        Args:
            code: ErrorCode 열거형
            details: 에러 상세 정보 (Pydantic 모델 또는 dict)
            status_code: HTTP 상태 코드 (기본값은 ErrorCode에 매핑된 값)
        """
        self.code = code
        self.status_code = status_code if status_code is not None else get_error_status(code)
        
        self.details = (
            details.model_dump() if isinstance(details, BaseModel) 
            else (details if details is not None else {})
        )

    def __str__(self):
        return f"[{self.code}] {self.status_code}: {self.details}"

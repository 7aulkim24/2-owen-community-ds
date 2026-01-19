"""
커스텀 예외 클래스 정의
- APIError 단일 클래스 통합
- ErrorCode 중심의 계층적 구조 지원
"""

from typing import Union, Optional, Any, Dict
from pydantic import BaseModel
from .error_codes import ErrorCode


class APIError(Exception):
    """모든 API 에러를 처리하는 단일 예외 클래스"""
    def __init__(
        self, 
        code: ErrorCode, 
        details: Union[BaseModel, Dict[str, Any], None] = None,
        message: Optional[str] = None,
        status_code: Optional[int] = None
    ):
        """
        Args:
            code: ErrorCode 열거형 (Category, StatusCode, Message 포함)
            details: 에러 상세 정보 (Pydantic 모델 또는 dict)
            message: 커스텀 에러 메시지 (지정하지 않으면 ErrorCode의 기본 메시지 사용)
            status_code: HTTP 상태 코드 (지정하지 않으면 ErrorCode의 기본 상태 코드 사용)
        """
        self.code = code
        self.category = code.category
        self.status_code = status_code if status_code is not None else code.status_code
        self.message = message if message is not None else code.default_message
        
        self.details = (
            details.model_dump() if isinstance(details, BaseModel) 
            else (details if details is not None else {})
        )

    def __str__(self):
        return f"[{self.code.name}] {self.status_code}: {self.message} (Category: {self.category})"

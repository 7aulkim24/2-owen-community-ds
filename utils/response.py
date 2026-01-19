"""
표준 API 응답 포맷
- Enum 기반 코드 사용
- 타입 안정성 확보
"""

from typing import Any, Dict, List
from .error_codes import ErrorCode, SuccessCode, get_success_message


class StandardResponse:
    """모든 API 응답의 표준 포맷"""

    @staticmethod
    def success(code: SuccessCode, data: Any = None) -> Dict:
        """
        성공 응답 생성
        
        Args:
            code: SuccessCode 열거형
            data: 응답 데이터
            
        Returns:
            표준 성공 응답 딕셔너리
        """
        return {
            "code": code.value,
            "message": get_success_message(code),
            "data": data if data is not None else {}
        }

    @staticmethod
    def error(code: ErrorCode, details: Dict = None) -> Dict:
        """
        에러 응답 생성
        
        Args:
            code: ErrorCode 열거형
            details: 상세 정보
            
        Returns:
            표준 에러 응답 딕셔너리
        """
        return {
            "code": code.value,
            "details": details if details is not None else {}
        }

    @staticmethod
    def validation_error(errors: List) -> Dict:
        """
        Pydantic 검증 실패 응답
        
        Args:
            errors: Pydantic ValidationError.errors() 결과
            
        Returns:
            표준 검증 에러 응답 딕셔너리
        """
        # ValidationError.errors()는 [{"type": "missing", "loc": ("email",), ...}] 형태
        field_errors = []
        for error in errors:
            field_errors.append({
                "field": error["loc"][-1],  # 마지막 경로가 필드명
                "type": error["type"],       # missing, value_error, type_error 등
                "message": error.get("msg", "Invalid value")
            })
        return {
            "code": ErrorCode.VALIDATION_ERROR.value,
            "details": {"fields": field_errors}
        }

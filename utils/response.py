"""
표준 API 응답 포맷
- Enum 기반 코드 사용
- 타입 안정성 확보
"""

from typing import Any, Dict, List
from .error_codes import ErrorCode, SuccessCode, get_error_message, get_success_message


class StandardResponse:
    """모든 API 응답의 표준 포맷"""

    @staticmethod
    def success(code: SuccessCode, data: Any = None, status_code: int = 200) -> Dict:
        """
        성공 응답 생성
        
        Args:
            code: SuccessCode 열거형
            data: 응답 데이터
            status_code: HTTP 상태 코드
            
        Returns:
            표준 성공 응답 딕셔너리
        """
        return {
            "status": "success",
            "code": code.value,
            "message": get_success_message(code),
            "data": data or {},
            "status_code": status_code
        }

    @staticmethod
    def error(code: ErrorCode, message: str = None, details: Dict = None, status_code: int = 400) -> Dict:
        """
        에러 응답 생성
        
        Args:
            code: ErrorCode 열거형
            message: 커스텀 메시지 (선택)
            details: 상세 정보
            status_code: HTTP 상태 코드
            
        Returns:
            표준 에러 응답 딕셔너리
        """
        return {
            "status": "error",
            "code": code.value,
            "message": message or get_error_message(code),
            "details": details or {},
            "status_code": status_code
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
            "status": "error",
            "code": ErrorCode.VALIDATION_ERROR.value,
            "message": get_error_message(ErrorCode.VALIDATION_ERROR),
            "fields": field_errors,
            "status_code": 422
        }

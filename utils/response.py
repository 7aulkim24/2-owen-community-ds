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
        """성공 응답 생성"""
        return {
            "code": code.value,
            "message": get_success_message(code),
            "data": data if data is not None else {}
        }

    @staticmethod
    def error(code: ErrorCode, details: Dict = None) -> Dict:
        """에러 응답 생성"""
        return {
            "code": code.value,
            "data": details if details is not None else None # 설계도 규격(data 필드 사용) 준수
        }

    @staticmethod
    def validation_error(errors: List) -> Dict:
        """
        Pydantic 검증 실패 응답 (설계도 60라인 규격 준수)
        """
        field_details = {}
        for error in errors:
            field_name = str(error["loc"][-1])
            error_type = error["type"]
            
            # 설계도 예시: "email": ["REQUIRED", "INVALID_FORMAT"]
            if field_name not in field_details:
                field_details[field_name] = []
            
            # Pydantic 에러 타입을 설계도 태그로 매핑
            tag = "INVALID_FORMAT"
            if "missing" in error_type:
                tag = "REQUIRED"
            elif "too_long" in error_type:
                tag = "TOO_LONG"
            elif "too_short" in error_type:
                tag = "TOO_SHORT"
                
            if tag not in field_details[field_name]:
                field_details[field_name].append(tag)
                
        return {
            "code": ErrorCode.INVALID_INPUT.value,
            "data": field_details
        }

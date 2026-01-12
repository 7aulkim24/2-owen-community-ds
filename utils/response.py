from typing import Any, Dict, List

class StandardResponse:
    """모든 API 응답의 표준 포맷"""

    @staticmethod
    def success(code: str, data: Any = None, status_code: int = 200) -> Dict:
        """성공 응답"""
        return {
            "status": "success",
            "code": code,
            "data": data or {},
            "status_code": status_code
        }

    @staticmethod
    def error(code: str, details: Dict = None, status_code: int = 400) -> Dict:
        """에러 응답"""
        return {
            "status": "error",
            "code": code,
            "details": details or {},
            "status_code": status_code
        }

    @staticmethod
    def validation_error(errors: List) -> Dict:
        """Pydantic 검증 실패 응답"""
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
            "code": "VALIDATION_ERROR",
            "fields": field_errors,
            "status_code": 422
        }
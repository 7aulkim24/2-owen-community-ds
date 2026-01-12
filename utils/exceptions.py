class APIException(Exception):
    """모든 커스텀 예외의 기본 클래스"""
    def __init__(self, code: str, status_code: int, details: dict = None):
        self.code = code
        self.status_code = status_code
        self.details = details or {}

class DuplicateEntryError(APIException):
    """409 Conflict: 중복된 데이터"""
    def __init__(self, field: str, value: str):
        super().__init__("DUPLICATE_ENTRY", 409, {"field": field, "value": value})

class UnauthorizedError(APIException):
    """401 Unauthorized: 인증 필요"""
    def __init__(self, message: str = "인증이 필요합니다"):
        super().__init__("UNAUTHORIZED", 401, {"message": message})

class ForbiddenError(APIException):
    """403 Forbidden: 권한 없음"""
    def __init__(self, message: str = "권한이 없습니다"):
        super().__init__("FORBIDDEN", 403, {"message": message})

class NotFoundError(APIException):
    """404 Not Found: 리소스 없음"""
    def __init__(self, resource: str):
        super().__init__("NOT_FOUND", 404, {"resource": resource})

class InvalidFormatError(APIException):
    """422 Unprocessable Entity: 형식 오류"""
    def __init__(self, field: str, reason: str):
        super().__init__("INVALID_FORMAT", 422, {"field": field, "reason": reason})
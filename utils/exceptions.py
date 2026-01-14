"""
커스텀 예외 클래스 정의
- 명시적인 에러 코드 전달
- 매직 로직 제거
- Enum 기반 타입 안정성
"""

from .error_codes import ErrorCode, get_error_message


class APIException(Exception):
    """모든 커스텀 예외의 기본 클래스"""
    def __init__(self, code: ErrorCode, status_code: int, details: dict = None):
        self.code = code
        self.message = get_error_message(code)
        self.status_code = status_code
        self.details = details or {}


class DuplicateEmailError(APIException):
    """409 Conflict: 이메일 중복"""
    def __init__(self, email: str):
        super().__init__(
            ErrorCode.DUPLICATE_EMAIL,
            409,
            {"field": "email", "value": email}
        )


class DuplicateNicknameError(APIException):
    """409 Conflict: 닉네임 중복"""
    def __init__(self, nickname: str):
        super().__init__(
            ErrorCode.DUPLICATE_NICKNAME,
            409,
            {"field": "nickname", "value": nickname}
        )


class DuplicateEntryError(APIException):
    """409 Conflict: 일반 중복 데이터"""
    def __init__(self, field: str, value: str = None):
        details = {"field": field}
        if value:
            details["value"] = value
        super().__init__(ErrorCode.DUPLICATE_ENTRY, 409, details)


class UnauthorizedError(APIException):
    """401 Unauthorized: 인증 필요"""
    def __init__(self, code: ErrorCode = ErrorCode.UNAUTHORIZED, details: dict = None):
        super().__init__(code, 401, details)


class ForbiddenError(APIException):
    """403 Forbidden: 권한 없음"""
    def __init__(self, code: ErrorCode = ErrorCode.FORBIDDEN, details: dict = None):
        super().__init__(code, 403, details)


class PostNotFoundError(APIException):
    """404 Not Found: 게시글 없음"""
    def __init__(self, post_id: str = None):
        details = {"resource": "게시글"}
        if post_id:
            details["post_id"] = post_id
        super().__init__(ErrorCode.POST_NOT_FOUND, 404, details)


class CommentNotFoundError(APIException):
    """404 Not Found: 댓글 없음"""
    def __init__(self, comment_id: str = None):
        details = {"resource": "댓글"}
        if comment_id:
            details["comment_id"] = comment_id
        super().__init__(ErrorCode.COMMENT_NOT_FOUND, 404, details)


class UserNotFoundError(APIException):
    """404 Not Found: 사용자 없음"""
    def __init__(self, user_id: str = None):
        details = {"resource": "사용자"}
        if user_id:
            details["user_id"] = user_id
        super().__init__(ErrorCode.USER_NOT_FOUND, 404, details)


class NotFoundError(APIException):
    """404 Not Found: 일반 리소스 없음"""
    def __init__(self, resource: str):
        super().__init__(ErrorCode.NOT_FOUND, 404, {"resource": resource})


class ValidationError(APIException):
    """422 Unprocessable Entity: 유효성 검증 실패"""
    def __init__(self, code: ErrorCode = ErrorCode.VALIDATION_ERROR, details: dict = None):
        super().__init__(code, 422, details)


class InvalidFormatError(APIException):
    """422 Unprocessable Entity: 형식 오류"""
    def __init__(self, field: str, reason: str):
        super().__init__(ErrorCode.INVALID_FORMAT, 422, {"field": field, "reason": reason})

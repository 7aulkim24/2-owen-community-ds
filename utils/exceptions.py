"""
커스텀 예외 클래스 정의
- 명시적인 에러 코드 전달
- 매직 로직 제거
- Enum 기반 타입 안정성
"""

from typing import Union, Optional
from pydantic import BaseModel
from .error_codes import ErrorCode, get_error_message
from schemas.error_schema import FieldError, ValidationErrorDetail, ResourceError


class APIException(Exception):
    """모든 커스텀 예외의 기본 클래스"""
    def __init__(self, code: ErrorCode, status_code: int, details: Union[BaseModel, dict, None] = None):
        self.code = code
        self.message = get_error_message(code)
        self.status_code = status_code
        
        if isinstance(details, BaseModel):
            self.details = details.model_dump()
        else:
            self.details = details or {}


class DuplicateEmailError(APIException):
    """409 Conflict: 이메일 중복"""
    def __init__(self, email: str):
        super().__init__(
            ErrorCode.DUPLICATE_EMAIL,
            409,
            FieldError(field="email", value=email)
        )


class DuplicateNicknameError(APIException):
    """409 Conflict: 닉네임 중복"""
    def __init__(self, nickname: str):
        super().__init__(
            ErrorCode.DUPLICATE_NICKNAME,
            409,
            FieldError(field="nickname", value=nickname)
        )


class DuplicateEntryError(APIException):
    """409 Conflict: 일반 중복 데이터"""
    def __init__(self, field: str, value: str = None):
        super().__init__(
            ErrorCode.DUPLICATE_ENTRY, 
            409, 
            FieldError(field=field, value=value)
        )


class UnauthorizedError(APIException):
    """401 Unauthorized: 인증 필요"""
    def __init__(self, code: ErrorCode = ErrorCode.UNAUTHORIZED, details: Union[BaseModel, dict, None] = None):
        super().__init__(code, 401, details)


class ForbiddenError(APIException):
    """403 Forbidden: 권한 없음"""
    def __init__(self, code: ErrorCode = ErrorCode.FORBIDDEN, details: Union[BaseModel, dict, None] = None):
        super().__init__(code, 403, details)


class PostNotFoundError(APIException):
    """404 Not Found: 게시글 없음"""
    def __init__(self, post_id: str = None):
        super().__init__(
            ErrorCode.POST_NOT_FOUND, 
            404, 
            ResourceError(resource="게시글", id=post_id)
        )


class CommentNotFoundError(APIException):
    """404 Not Found: 댓글 없음"""
    def __init__(self, comment_id: str = None):
        super().__init__(
            ErrorCode.COMMENT_NOT_FOUND, 
            404, 
            ResourceError(resource="댓글", id=comment_id)
        )


class UserNotFoundError(APIException):
    """404 Not Found: 사용자 없음"""
    def __init__(self, user_id: str = None):
        super().__init__(
            ErrorCode.USER_NOT_FOUND, 
            404, 
            ResourceError(resource="사용자", id=user_id)
        )


class NotFoundError(APIException):
    """404 Not Found: 일반 리소스 없음"""
    def __init__(self, resource: str):
        super().__init__(ErrorCode.NOT_FOUND, 404, ResourceError(resource=resource))


class ValidationError(APIException):
    """422 Unprocessable Entity: 유효성 검증 실패"""
    def __init__(self, code: ErrorCode = ErrorCode.VALIDATION_ERROR, details: Union[BaseModel, dict, None] = None):
        super().__init__(code, 422, details)


class InvalidFormatError(APIException):
    """422 Unprocessable Entity: 형식 오류"""
    def __init__(self, field: str, reason: str):
        super().__init__(
            ErrorCode.INVALID_FORMAT, 
            422, 
            ValidationErrorDetail(field=field, reason=reason)
        )

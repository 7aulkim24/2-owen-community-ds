"""
에러 코드와 성공 코드 정의 (Enum 기반)
- 타입 안정성 확보
- IDE 자동완성 지원
- 에러/성공 메시지 분리 관리
"""

from enum import Enum


class ErrorCode(str, Enum):
    """에러 코드 열거형"""
    
    # 400 Bad Request
    INVALID_INPUT = "INVALID_INPUT"
    MISSING_FIELD = "MISSING_FIELD"
    INVALID_FORMAT = "INVALID_FORMAT"
    
    # 401 Unauthorized
    UNAUTHORIZED = "UNAUTHORIZED"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    SESSION_EXPIRED = "SESSION_EXPIRED"
    INVALID_SESSION = "INVALID_SESSION"
    
    # 403 Forbidden
    FORBIDDEN = "FORBIDDEN"
    NOT_OWNER = "NOT_OWNER"
    
    # 404 Not Found
    NOT_FOUND = "NOT_FOUND"
    POST_NOT_FOUND = "POST_NOT_FOUND"
    COMMENT_NOT_FOUND = "COMMENT_NOT_FOUND"
    USER_NOT_FOUND = "USER_NOT_FOUND"
    
    # 409 Conflict
    DUPLICATE_ENTRY = "DUPLICATE_ENTRY"
    DUPLICATE_EMAIL = "DUPLICATE_EMAIL"
    DUPLICATE_NICKNAME = "DUPLICATE_NICKNAME"
    
    # 422 Unprocessable Entity
    VALIDATION_ERROR = "VALIDATION_ERROR"
    EMPTY_CONTENT = "EMPTY_CONTENT"
    TITLE_TOO_SHORT = "TITLE_TOO_SHORT"
    TITLE_TOO_LONG = "TITLE_TOO_LONG"
    PASSWORD_TOO_SHORT = "PASSWORD_TOO_SHORT"
    
    # 500 Internal Server Error
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"


class SuccessCode(str, Enum):
    """성공 코드 열거형"""
    
    # Health Check
    HEALTH_CHECK_OK = "HEALTH_CHECK_OK"
    
    # 게시글 관련
    GET_POSTS_SUCCESS = "GET_POSTS_SUCCESS"
    GET_POST_SUCCESS = "GET_POST_SUCCESS"
    POST_CREATED = "POST_CREATED"
    POST_UPDATED = "POST_UPDATED"
    POST_DELETED = "POST_DELETED"
    
    # 댓글 관련
    COMMENTS_RETRIEVED = "COMMENTS_RETRIEVED"
    COMMENT_CREATED = "COMMENT_CREATED"
    COMMENT_UPDATED = "COMMENT_UPDATED"
    COMMENT_DELETED = "COMMENT_DELETED"
    
    # 사용자 관련
    GET_USER_SUCCESS = "GET_USER_SUCCESS"
    LOGIN_SUCCESS = "LOGIN_SUCCESS"
    LOGOUT_SUCCESS = "LOGOUT_SUCCESS"
    SIGNUP_SUCCESS = "SIGNUP_SUCCESS"


# 에러 상태 코드 매핑
ERROR_STATUS_MAP = {
    ErrorCode.INVALID_INPUT: 400,
    ErrorCode.MISSING_FIELD: 400,
    ErrorCode.INVALID_FORMAT: 400,
    
    ErrorCode.UNAUTHORIZED: 401,
    ErrorCode.INVALID_CREDENTIALS: 401,
    ErrorCode.SESSION_EXPIRED: 401,
    ErrorCode.INVALID_SESSION: 401,
    
    ErrorCode.FORBIDDEN: 403,
    ErrorCode.NOT_OWNER: 403,
    
    ErrorCode.NOT_FOUND: 404,
    ErrorCode.POST_NOT_FOUND: 404,
    ErrorCode.COMMENT_NOT_FOUND: 404,
    ErrorCode.USER_NOT_FOUND: 404,
    
    ErrorCode.DUPLICATE_ENTRY: 409,
    ErrorCode.DUPLICATE_EMAIL: 409,
    ErrorCode.DUPLICATE_NICKNAME: 409,
    
    ErrorCode.VALIDATION_ERROR: 422,
    ErrorCode.EMPTY_CONTENT: 422,
    ErrorCode.TITLE_TOO_SHORT: 422,
    ErrorCode.TITLE_TOO_LONG: 422,
    ErrorCode.PASSWORD_TOO_SHORT: 422,
    
    ErrorCode.INTERNAL_SERVER_ERROR: 500,
}

# 성공 메시지 매핑
SUCCESS_MESSAGES = {
    SuccessCode.HEALTH_CHECK_OK: "서버가 정상적으로 작동 중입니다.",
    
    SuccessCode.GET_POSTS_SUCCESS: "게시글 목록을 성공적으로 조회했습니다.",
    SuccessCode.GET_POST_SUCCESS: "게시글을 성공적으로 조회했습니다.",
    SuccessCode.POST_CREATED: "게시글이 작성되었습니다.",
    SuccessCode.POST_UPDATED: "게시글이 수정되었습니다.",
    SuccessCode.POST_DELETED: "게시글이 삭제되었습니다.",
    
    SuccessCode.COMMENTS_RETRIEVED: "댓글 목록을 성공적으로 조회했습니다.",
    SuccessCode.COMMENT_CREATED: "댓글이 작성되었습니다.",
    SuccessCode.COMMENT_UPDATED: "댓글이 수정되었습니다.",
    SuccessCode.COMMENT_DELETED: "댓글이 삭제되었습니다.",
    
    SuccessCode.GET_USER_SUCCESS: "사용자 정보를 성공적으로 조회했습니다.",
    SuccessCode.LOGIN_SUCCESS: "로그인에 성공했습니다.",
    SuccessCode.LOGOUT_SUCCESS: "로그아웃되었습니다.",
    SuccessCode.SIGNUP_SUCCESS: "회원가입이 완료되었습니다.",
}


def get_error_status(code: ErrorCode) -> int:
    """
    에러 코드에 해당하는 HTTP 상태 코드 반환
    
    Args:
        code: ErrorCode 열거형
        
    Returns:
        HTTP 상태 코드 (기본값 400)
    """
    return ERROR_STATUS_MAP.get(code, 400)


def get_success_message(code: SuccessCode) -> str:
    """
    성공 코드에 해당하는 메시지 반환
    
    Args:
        code: SuccessCode 열거형
        
    Returns:
        성공 메시지 문자열
    """
    return SUCCESS_MESSAGES.get(code, "요청이 성공적으로 처리되었습니다.")

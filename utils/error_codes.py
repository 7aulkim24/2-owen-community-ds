from enum import Enum


class ErrorCode(Enum):
    """에러 코드 열거형 (계층화 및 세분화 버전)"""
    
    # (카테고리, 상태코드, 기본 메시지)
    
    # --- 공통 및 시스템 에러 ---
    BAD_REQUEST = ("COMMON", 400, "잘못된 요청입니다.")
    UNAUTHORIZED = ("AUTH", 401, "로그인이 필요합니다.")
    FORBIDDEN = ("AUTH", 403, "권한이 없습니다.")
    NOT_FOUND = ("COMMON", 404, "요청하신 리소스를 찾을 수 없습니다.")
    METHOD_NOT_ALLOWED = ("COMMON", 405, "허용되지 않은 메서드입니다.")
    TOO_MANY_REQUEST = ("SYSTEM", 429, "너무 많은 요청이 발생했습니다.")
    INTERNAL_SERVER_ERROR = ("SYSTEM", 500, "서버 내부 오류가 발생했습니다.")

    # --- 검증 에러 ---
    INVALID_INPUT = ("VALIDATION", 422, "입력 값이 올바르지 않습니다.")

    # --- 인증 관련 핵심 도메인 에러 ---
    INVALID_CREDENTIALS = ("AUTH", 401, "이메일 또는 비밀번호가 일치하지 않습니다.")
    ALREADY_LOGIN = ("AUTH", 409, "이미 로그인된 상태입니다.")
    EMAIL_ALREADY_EXISTS = ("USER", 409, "이미 사용 중인 이메일입니다.")
    NICKNAME_ALREADY_EXISTS = ("USER", 409, "이미 사용 중인 닉네임입니다.")

    # --- 리소스 존재 여부 핵심 에러 ---
    USER_NOT_FOUND = ("USER", 404, "사용자를 찾을 수 없습니다.")
    POST_NOT_FOUND = ("POST", 404, "게시글을 찾을 수 없습니다.")
    COMMENT_NOT_FOUND = ("COMMENT", 404, "댓글을 찾을 수 없습니다.")

    # --- 기타 설계도 명시 특수 에러 ---
    POST_ALREADY_LIKED = ("POST", 409, "이미 좋아요를 누른 게시글입니다.")
    POST_ALREADY_UNLIKED = ("POST", 409, "좋아요를 누르지 않은 게시글입니다.")
    PAYLOAD_TOO_LARGE = ("SYSTEM", 413, "파일 크기가 너무 큽니다.")
    RATE_LIMIT_EXCEEDED = ("SYSTEM", 429, "요청 빈도가 너무 높습니다.")

    @property
    def category(self) -> str:
        return self.value[0]

    @property
    def status_code(self) -> int:
        return self.value[1]

    @property
    def default_message(self) -> str:
        return self.value[2]


class SuccessCode(str, Enum):
    """성공 코드 열거형 (최적화 버전)"""
    
    SIGNUP_SUCCESS = "SIGNUP_SUCCESS"
    LOGIN_SUCCESS = "LOGIN_SUCCESS"
    AUTH_SUCCESS = "AUTH_SUCCESS"
    EMAIL_AVAILABLE = "EMAIL_AVAILABLE"
    NICKNAME_AVAILABLE = "NICKNAME_AVAILABLE"
    
    USER_FETCHED = "USER_FETCHED"
    USER_RETRIEVED = "USER_RETRIEVED"
    USER_UPDATED = "USER_UPDATED"
    USER_PASSWORD_UPDATED = "USER_PASSWORD_UPDATED"
    PROFILE_IMAGE_UPLOADED = "PROFILE_IMAGE_UPLOADED"
    
    POSTS_RETRIEVED = "POSTS_RETRIEVED"
    POST_RETRIEVED = "POST_RETRIEVED"
    POST_CREATED = "POST_CREATED"
    POST_UPDATED = "POST_UPDATED"
    POST_DELETED = "POST_DELETED"
    POST_FILE_UPLOADED = "POST_FILE_UPLOADED"
    POST_LIKE_CREATED = "POST_LIKE_CREATED"
    POST_LIKE_DELETED = "POST_LIKE_DELETED"
    POST_LIKE_UPDATED = "POST_LIKE_UPDATED"
    
    COMMENTS_RETRIEVED = "COMMENTS_RETRIEVED"
    COMMENT_CREATED = "COMMENT_CREATED"
    COMMENT_UPDATED = "COMMENT_UPDATED"
    COMMENT_DELETED = "COMMENT_DELETED"
    
    LOGOUT_SUCCESS = "LOGOUT_SUCCESS"
    HEALTH_CHECK_OK = "HEALTH_CHECK_OK"


def get_error_status(code: ErrorCode) -> int:
    """하위 호환성을 위한 함수"""
    return code.status_code


def get_success_message(code: SuccessCode) -> str:
    return "요청이 성공적으로 처리되었습니다."

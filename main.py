"""
FastAPI 애플리케이션 메인 파일
- 예외 처리 핸들러
- CORS 설정
- 라우터 등록
"""

import logging
import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from config import settings

from utils.exceptions import APIError
from utils.response import StandardResponse
from utils.error_codes import ErrorCode, SuccessCode
from utils.auth_middleware import AuthMiddleware

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Owen Community Backend",
    description="FastAPI 기반 커뮤니티 백엔드 API",
    version="1.0.0"
)

# 정적 파일 서빙 (이미지 업로드 등)
UPLOAD_DIR = "public"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)
    os.makedirs(os.path.join(UPLOAD_DIR, "image/post"))
    os.makedirs(os.path.join(UPLOAD_DIR, "image/profile"))

app.mount("/public", StaticFiles(directory=UPLOAD_DIR), name="public")

# 인증 미들웨어 등록 (세션 미들웨어보다 먼저 등록되어야 함을 주의 - FastAPI는 거꾸로 실행됨)
app.add_middleware(AuthMiddleware)

# 세션 설정 (로컬 개발 환경 기준)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.secret_key,
    https_only=settings.cookie_secure,
    same_site=settings.cookie_samesite,
    max_age=settings.session_timeout
)

# CORS 설정 (프론트엔드 연동)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",     # React
        "http://localhost:5173",     # Vite
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,          # 쿠키 자동 전송
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic 검증 실패 처리 (요청 형식 오류)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    요청 본문 검증 실패 시 발동
    예: 이메일 필드가 없거나, 형식이 잘못됨
    """
    logger.warning(f"Validation error at {request.url}: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content=StandardResponse.validation_error(exc.errors())
    )

# 커스텀 API 예외 처리 (비즈니스 로직 오류)
@app.exception_handler(APIError)
async def api_exception_handler(request: Request, exc: APIError):
    """
    Service에서 명시적으로 발생시킨 예외 처리
    예: 중복된 이메일, 권한 없음, 리소스 없음
    """
    logger.info(f"API error at {request.url}: {exc.code.name}")
    return JSONResponse(
        status_code=exc.status_code,
        content=StandardResponse.error(exc.code, exc.details, exc.message)
    )

# 예상치 못한 서버 오류
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    모든 예상 밖의 오류를 500으로 처리하고 로깅
    """
    # Stack Trace를 포함한 로깅
    logger.error(
        f"Unexpected error at {request.url}: {str(exc)}",
        exc_info=True  # Stack trace 포함
    )
    
    return JSONResponse(
        status_code=500,
        content=StandardResponse.error(ErrorCode.INTERNAL_SERVER_ERROR, {})
    )

# 헬스 체크 엔드포인트
@app.get("/health")
async def health_check():
    """서버 상태 확인"""
    return StandardResponse.success(SuccessCode.HEALTH_CHECK_OK, {"status": "healthy"})

# 라우터 등록
from routers import post_router, comment_router, auth_router, user_router

app.include_router(post_router)
app.include_router(comment_router)
app.include_router(auth_router)
app.include_router(user_router)

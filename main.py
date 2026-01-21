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
from utils.request_id_middleware import RequestIDMiddleware, request_id_ctx

# 로깅 필터: 로그에 request_id 추가
class RequestIDFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request_id_ctx.get()
        return True

# 로깅 설정
logging_handler = logging.StreamHandler()
logging_handler.addFilter(RequestIDFilter())
logging_handler.setFormatter(logging.Formatter(
    '%(asctime)s - [%(request_id)s] - %(name)s - %(levelname)s - %(message)s'
))

logging.basicConfig(
    level=logging.INFO,
    handlers=[logging_handler],
    force=True
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Owen Community Backend",
    description="FastAPI 기반 커뮤니티 백엔드 API",
    version="1.0.0"
)

# 정적 파일 서빙
UPLOAD_DIR = "public"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)
    os.makedirs(os.path.join(UPLOAD_DIR, "image/post"))
    os.makedirs(os.path.join(UPLOAD_DIR, "image/profile"))

app.mount("/public", StaticFiles(directory=UPLOAD_DIR), name="public")

# 미들웨어 등록 (LIFO 순서로 실행됨: RequestID -> CORS -> Session -> Auth -> App)
app.add_middleware(AuthMiddleware)
app.add_middleware(SessionMiddleware, 
                   secret_key=settings.secret_key,
                   https_only=settings.cookie_secure,
                   same_site=settings.cookie_samesite,
                   max_age=settings.session_timeout)
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])
app.add_middleware(RequestIDMiddleware)

# 예외 핸들러
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content=StandardResponse.validation_error(exc.errors())
    )

@app.exception_handler(APIError)
async def api_exception_handler(request: Request, exc: APIError):
    logger.info(f"API error: {exc.code.name}")
    return JSONResponse(
        status_code=exc.status_code,
        content=StandardResponse.error(exc.code, exc.details, exc.message)
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=StandardResponse.error(ErrorCode.INTERNAL_SERVER_ERROR, {})
    )

@app.get("/health")
async def health_check():
    return StandardResponse.success(SuccessCode.SUCCESS, {"status": "healthy"})

# 라우터 등록
from routers import post_router, comment_router, auth_router, user_router
app.include_router(post_router)
app.include_router(comment_router)
app.include_router(auth_router)
app.include_router(user_router)

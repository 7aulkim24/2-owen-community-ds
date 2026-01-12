from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from utils.exceptions import APIException
from utils.response import StandardResponse

app = FastAPI(
    title="Owen Community Backend",
    description="FastAPI 기반 커뮤니티 백엔드 API",
    version="1.0.0"
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
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    """
    요청 본문 검증 실패 시 발동
    예: 이메일 필드가 없거나, 형식이 잘못됨
    """
    # ValidationError.errors()는 필드별 상세 정보 포함
    # MISSING_FIELD: 필드 자체가 없음
    # INVALID_FORMAT: 형식 규칙 위반
    return JSONResponse(
        status_code=422,
        content=StandardResponse.validation_error(exc.errors())
    )

# 커스텀 API 예외 처리 (비즈니스 로직 오류)
@app.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException):
    """
    Service에서 명시적으로 발생시킨 예외 처리
    예: 중복된 이메일, 권한 없음, 리소스 없음
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=StandardResponse.error(exc.code, exc.details)
    )

# 예상치 못한 서버 오류
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """모든 예상 밖의 오류를 500으로 처리"""
    return JSONResponse(
        status_code=500,
        content=StandardResponse.error("INTERNAL_SERVER_ERROR", {})
    )

# 헬스 체크 엔드포인트
@app.get("/health")
async def health_check():
    """서버 상태 확인"""
    return StandardResponse.success("HEALTH_CHECK_OK", {"status": "healthy"})

# 라우터 등록
from routers.post_router import router as post_router

app.include_router(post_router)

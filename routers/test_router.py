from fastapi import APIRouter, status
from utils.test.test_utils import seed_database
from utils.common.response import StandardResponse
from utils.errors.error_codes import SuccessCode

router = APIRouter(prefix="/v1/test", tags=["테스트 유틸리티"])

@router.post("/reset", status_code=status.HTTP_200_OK)
async def reset_database():
    """인메모리 데이터베이스 초기화 및 시드 데이터 삽입 (테스트용)"""
    data = seed_database()
    return StandardResponse.success(SuccessCode.SUCCESS, data)

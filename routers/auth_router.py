from fastapi import APIRouter, Request, status, Query
from typing import Dict
from utils.response import StandardResponse
from utils.error_codes import SuccessCode
from controllers.auth_controller import auth_controller
from schemas.auth_schema import SignupRequest, LoginRequest, UserResponse, EmailAvailabilityResponse, NicknameAvailabilityResponse
from schemas.base_schema import StandardResponse as StandardResponseSchema

router = APIRouter(prefix="/v1/auth", tags=["인증"])


@router.post("/signup", response_model=StandardResponseSchema[UserResponse], status_code=status.HTTP_201_CREATED)
async def signup(req: SignupRequest):
    """회원가입"""
    data = auth_controller.signup(req)
    return StandardResponse.success(SuccessCode.SIGNUP_SUCCESS, data)


@router.post("/login", response_model=StandardResponseSchema[UserResponse], status_code=status.HTTP_200_OK)
async def login(req: LoginRequest, request: Request):
    """로그인"""
    data = auth_controller.login(req, request)
    return StandardResponse.success(SuccessCode.LOGIN_SUCCESS, data)


@router.post("/logout", response_model=StandardResponseSchema[Dict], status_code=status.HTTP_200_OK)
async def logout(request: Request):
    """로그아웃"""
    data = auth_controller.logout(request)
    return StandardResponse.success(SuccessCode.LOGOUT_SUCCESS, data)


@router.get("/me", response_model=StandardResponseSchema[UserResponse], status_code=status.HTTP_200_OK)
async def get_me(request: Request):
    """내 정보 조회 (로그인 상태 검증)"""
    data = auth_controller.getMe(request)
    return StandardResponse.success(SuccessCode.USER_RETRIEVED, data)


@router.get("/emails/availability", response_model=StandardResponseSchema[EmailAvailabilityResponse], status_code=status.HTTP_200_OK)
async def check_email_availability(email: str = Query(..., description="중복 확인할 이메일")):
    """이메일 중복 체크"""
    data = auth_controller.checkEmailAvailability(email)
    return StandardResponse.success(SuccessCode.EMAIL_AVAILABLE, data)


@router.get("/nicknames/availability", response_model=StandardResponseSchema[NicknameAvailabilityResponse], status_code=status.HTTP_200_OK)
async def check_nickname_availability(nickname: str = Query(..., description="중복 확인할 닉네임")):
    """닉네임 중복 체크"""
    data = auth_controller.checkNicknameAvailability(nickname)
    return StandardResponse.success(SuccessCode.NICKNAME_AVAILABLE, data)

from fastapi import APIRouter, Request, status
from typing import Dict
from utils.response import StandardResponse
from utils.error_codes import SuccessCode
from controllers.auth_controller import auth_controller
from schemas.auth_schema import SignupRequest, LoginRequest

router = APIRouter(prefix="/v1/auth", tags=["인증"])


@router.post("/signup", response_model=None, status_code=status.HTTP_201_CREATED)
async def signup(req: SignupRequest):
    """회원가입"""
    data = auth_controller.signup(req)
    return StandardResponse.success(SuccessCode.SIGNUP_SUCCESS, data, 201)


@router.post("/login", response_model=None, status_code=status.HTTP_200_OK)
async def login(req: LoginRequest, request: Request):
    """로그인"""
    data = auth_controller.login(req, request)
    return StandardResponse.success(SuccessCode.LOGIN_SUCCESS, data)


@router.post("/logout", response_model=None, status_code=status.HTTP_200_OK)
async def logout(request: Request):
    """로그아웃"""
    data = auth_controller.logout(request)
    return StandardResponse.success(SuccessCode.LOGOUT_SUCCESS, data)


@router.get("/me", response_model=None, status_code=status.HTTP_200_OK)
async def get_me(request: Request):
    """내 정보 조회"""
    data = auth_controller.get_me(request)
    return StandardResponse.success(SuccessCode.GET_USER_SUCCESS, data)

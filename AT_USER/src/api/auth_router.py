from fastapi import APIRouter, Depends, HTTPException

from src.dto.db.user import DTOUserDB
from src.service.interface import UserServiceInterface
from src.service.user.user import UserService
from src.dto.api.auth import (
    SignInRequest,
    SignUpRequest,
    SignInResponse,
    SignUpResponse,
)


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/sign_in", response_model=SignInResponse)
async def sign_in(
    body: SignInRequest, user_service: UserServiceInterface = Depends(UserService)
):
    try:
        token = user_service.generate_token(
            body.login,
            body.password,
        )
    except ValueError:
        raise HTTPException(status_code=401, detail="Login failed")
    return SignInResponse(token=token)


@router.post("/sign_up", response_model=SignUpResponse)
async def sign_up(
    body: SignUpRequest, user_service: UserServiceInterface = Depends(UserService)
):
    user_id = user_service.create_user(
        DTOUserDB(
            id=0,
            login=body.login,
            password=body.password,
            email=body.email,
            group=body.group,
        )
    )
    return SignUpResponse(user_id=user_id)

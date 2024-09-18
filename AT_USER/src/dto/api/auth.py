from pydantic import BaseModel, EmailStr


class SignInRequest(BaseModel):
    login: str
    password: str


class SignUpRequest(BaseModel):
    login: str
    password: str
    email: EmailStr
    group: str


class SignInResponse(BaseModel):
    token: str


class SignUpResponse(BaseModel):
    user_id: int

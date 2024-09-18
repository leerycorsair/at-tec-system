import datetime
from fastapi import Depends
import jwt
from passlib.context import CryptContext
from pydantic import EmailStr
from src.dto.db.user import DTOUserDB
from src.repository.interface import UserRepositoryInterface
from src.repository.user import UserRepository
from src.service.user.config import authConfig


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, rep: UserRepositoryInterface = Depends(UserRepository)):
        self._rep = rep

    def create_user(self, user: DTOUserDB) -> int:
        self._verify_email(user.email)
        user.password = self._generate_password_hash(user.password)
        return self._rep.create_user(user)

    def generate_token(self, login: str, password: str) -> str:
        user = self._rep.get_user(login)
        if not user or not self._verify_password(
            plain_password=password,
            hashed_password=user.password,
        ):
            raise ValueError("Incorrect password")
        access_token_expires = datetime.timedelta(
            minutes=authConfig.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        token = self._create_token(
            data={"user_id": user.id},
            expires_delta=access_token_expires,
        )
        return token

    def verify_token(self, token: str) -> int:
        try:
            decoded = jwt.decode(
                token,
                key=authConfig.SECRET_KEY,
                algorithms=[authConfig.ALGORITHM],
            )
            return decoded["user_id"]
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")

    def _generate_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)

    def _create_token(self, data: dict, expires_delta: datetime.timedelta) -> str:
        to_encode = data.copy()
        expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
        return jwt.encode(
            to_encode,
            key=authConfig.SECRET_KEY,
            algorithm=authConfig.ALGORITHM,
        )

    def _verify_email(self, email: EmailStr):
        email_str = str(email)
        if not email_str.endswith("@campus.mephi.ru"):
            raise ValueError("MEPhI email required")

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

from pydantic import BaseModel, EmailStr


class DTOUserDB(BaseModel):
    id: int
    login: str
    password: str
    email: EmailStr
    group: str

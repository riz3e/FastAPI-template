from typing import Union

from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Union[str, None] = None #email btw, not id


class User(BaseModel):
    email: EmailStr
    name: str
    surname: str
    hashed_password: str = Field(min_length=8)
    is_teacher: bool = False
    grade: int = Field(le=12, ge=7)  # from the 7 to 12 grade
    letter: str = Field(max_length=1)


class UserInDB(User):
    hashed_password: str

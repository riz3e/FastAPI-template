from typing import Union

from pydantic import BaseModel, EmailStr, Field


class User(BaseModel): #DataToObj class
    email: EmailStr
    name: str
    surname: str
    hashed_password: str = Field(min_length=8)
    is_teacher: bool = False
    grade: int = Field(le=12, ge=7) # from the 7 to 12 grade
    letter: str = Field(max_length=1)

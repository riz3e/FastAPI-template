# from datetime import datetime, timedelta
import datetime as dt
from typing import Union, Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from database import get_db
from dto.oauth import UserInDB, TokenData, Token, User
from models.user import User as UserDB

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_user_id_by_email(email: str, db: Session):
    user = db.query(UserDB).filter(UserDB.email == email).first()
    if user:
        return user.id
    return None


def get_user(db, id: int):
    user = db.query(UserDB).filter(UserDB.id == id).first()
    if user:
        # print(user)
        user_dict = user.__dict__

        user_dict.pop('_sa_instance_state', None)
        # print(user_dict)
        return UserInDB(**user_dict)
        # return UserInDB(**user)  # Simplified with dictionary unpacking
    return None


def authenticate_user(id: int, password: str, db: Session):
    user = get_user(id=id, db=db)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[dt.timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = dt.datetime.utcnow() + expires_delta
    else:
        expire = dt.datetime.utcnow() + dt.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(id=username)
    except JWTError:
        raise credentials_exception
    user_id = get_user_id_by_email(token_data.id, db=db)
    user = get_user(id=user_id, db=db)
    if user is None:
        raise credentials_exception
    return user

# async def get_current_active_user(
#         current_user: Annotated[User, Depends(get_current_user)]
# ):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user

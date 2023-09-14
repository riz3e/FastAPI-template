import datetime as dt
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from config import ACCESS_TOKEN_EXPIRE_MINUTES
from database import get_db
from dto.oauth import Token, User
from services.oauth import get_user_id_by_email, verify_password, get_user, authenticate_user, create_access_token, \
    get_current_user

router = APIRouter()



@router.post("/token", response_model=Token, tags=["oauth"])
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    id = get_user_id_by_email(form_data.username, db=db)
    print(id)
    print(verify_password(form_data.password, hashed_password=get_user(id=id, db=db).hashed_password))
    user = authenticate_user(id=id,
                             password=form_data.password, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = dt.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=User, tags=["oauth"])
async def read_users_me(
        current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user
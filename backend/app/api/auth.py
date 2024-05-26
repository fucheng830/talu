# token_manager.py
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import os
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from fastapi import APIRouter
from ..utils import md5
from fastapi.encoders import jsonable_encoder

router = APIRouter()

# 在这里定义你的密钥。在实际应用中，你会希望这是一个环境变量，以确保安全。
SECRET_KEY = os.environ.get("SECRET_KEY") or "your_secret_key"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=180)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm='HS256')
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY)
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = authenticate_user(user_id, payload.get("password"), db)
    if not user:
        raise credentials_exception
    
    user_dict = jsonable_encoder(user)  # Convert the user object to a dictionary
    user_dict['token'] = token  # Add the token to the dictionary
    
    return user_dict

def authenticate_user(user_id: str, password: str, db: Session):
    # 这里添加用户验证逻辑，如查询数据库
    # 查询数据库 
    user = db.query(User).filter_by(user_id=user_id).first()
    if user:
        return user


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=form_data.username, password=md5(form_data.password)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"user_id": str(user.user_id),
              "password": form_data.password
              }
    )
    return {"access_token": access_token, "token_type": "bearer"}

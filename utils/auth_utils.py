from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError,jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from fastapi import Depends, HTTPException,status
import os

from sqlmodel import Session, select
from config.db import get_session
from models.tables import User



SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user(db:Session, username: str):
    return db.exec(select(User).where(User.username == username)).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user or not verify_password(password, user.password):
        return False
    return user

async def get_current_user(token: str = Depends(oauth2_scheme),session:Session=Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise credentials_exception
        
        user = session.exec(select(User).where(User.username == username)).first()
        if user is None:
            raise credentials_exception

        return user
    except JWTError:
        raise credentials_exception












































# SECRET_KEY = os.getenv('SECRET_KEY')
# ALGORITHM = os.getenv('ALGORITHM')
# ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# def verify_password(plain_password,hashed_password):
#     return pwd_context.verify(plain_password,hashed_password)

# def hash_password(password):
#     return pwd_context.hash(password)

# # def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
# #     try:
# #         to_encode = data.copy()
# #         if expires_delta:
# #             expire = datetime.now(timezone.utc) + expires_delta
# #         else:
# #             expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
# #         to_encode.update({"exp": expire})
# #         encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
# #         return encoded_jwt
# #     except Exception as e:
# #         return None
    
# def create_access_token(user_id: int, expires_delta: Optional[timedelta] = None):
#     try:
#         expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
#         to_encode = {
#             "sub": str(user_id),
#             "exp": expire
#         }
#         encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#         return encoded_jwt
#     except Exception as e:
#         print(f"Token creation error: {e}")
#         return None



# def verify_token(token: str = Depends(oauth2_scheme),session:Session=Depends(get_session)):
#     try:
#         decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # type: ignore
#         user_id = decoded_token.get("sub")  # or "id" depending on your token
#         if user_id is None:
#             raise HTTPException(status_code=401, detail="Invalid token payload")

#         user = session.exec(select(User).where(User.id == int(user_id))).first()
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found")

#         return user
#     except jwt.ExpiredSignatureError:
#         raise HTTPException(status_code=401, detail="Token expired")
#     except jwt.InvalidTokenError:
#         raise HTTPException(status_code=401, detail="Invalid token")
#     except Exception:
#         raise HTTPException(status_code=401, detail="Invalid token")

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from config.db import get_session
from models.schema import UserCreate
from models.tables import User
from utils.auth_utils import authenticate_user, create_access_token, get_password_hash

user_router = APIRouter()

@user_router.post("/register")
def create_user(user_data:UserCreate,session:Session=Depends(get_session)):
    try:
        exist_user = session.exec(select(User).where((User.username==user_data.username) | (User.email==user_data.email))).first()
        if exist_user:
            raise HTTPException(status_code=400, detail="User already exists")
        user_hash_password = get_password_hash(user_data.password)
        
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            password=user_hash_password,
            role=user_data.role,
            created_at=user_data.created_at
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return {"message":"User created successfully","data":new_user}
    except Exception as e:
        return{
            "message": str(e),
            "status": "error",
            "data": None
        }

@user_router.post("/login")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
        try:
            user = authenticate_user(session, form_data.username, form_data.password)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            access_token_expires = timedelta(minutes=30)
            access_token = create_access_token(
                data={"sub": user.username,"role": user.role}, expires_delta=access_token_expires
            )
            return {"access_token": access_token, "token_type": "bearer"}
        except Exception as e:
            return {
            "message": str(e),
            "status": "error",
            "data": None
            }













































# def login_user(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
#     print(f"Received login request: {form_data}")  # Log the incoming form data
#     try:
#         db_user = session.exec(select(User).where(User.username == form_data.username)).first()
#         if not db_user:
#             raise HTTPException(status_code=400, detail="User not Found")
#         valid_password = verify_password(form_data.password, db_user.password)
#         if not valid_password:
#             raise HTTPException(status_code=400, detail="Invalid password")
        
#         access_token_expires = timedelta(minutes=30)
#         token = create_access_token(data={"sub": str(db_user.id),"role": db_user.role}, expires_delta=access_token_expires)
#         return {"access_token": token, "token_type": "bearer"}
#     except Exception as e:
#         print(f"Error during login: {e}")
#         return {
#             "message": str(e),
#             "status": "error",
#             "data": None
#         }

        
            
        
        

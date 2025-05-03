from sqlmodel import Field
from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum
from typing import Optional

    
#User Schema

class UserRole(str,Enum):
    USER = "user"
    ADMIN = "admin"

class UserCreate(BaseModel):
    username : str = Field(index=True,unique=True)
    email : EmailStr
    password : str
    role : UserRole =Field(default=UserRole.USER)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    

#Contact Schema

class ContactCreate(BaseModel):
    name : str
    phone : Optional[str]
    email : Optional[str]
    created_at : datetime = Field(default_factory=datetime.utcnow)
    
class ContactUpdate(BaseModel):
    name : str
    phone : Optional[str]
    email : Optional[str]
    updated_at : datetime = Field(default_factory=datetime.utcnow)
    
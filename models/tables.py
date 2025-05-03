from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, SQLModel , Relationship
from pydantic import EmailStr

from models.schema import UserRole

class User(SQLModel,table=True):
    __tablename__ = 'users'
    id : Optional[int] = Field(default=None,primary_key=True,index=True)
    username : str = Field(index=True,unique=True)
    email : EmailStr
    password : str
    role : UserRole =Field(default=UserRole.USER)
    created_at: datetime = Field(default_factory=datetime.utcnow)
 
    contacts : List["Contact"] =Relationship(back_populates="user")
    
class Contact(SQLModel,table=True):
    __tablename__ = 'contacts'
    id : Optional[int] = Field(default=None,primary_key=True,index=True)
    user_id : int = Field(foreign_key="users.id")
    name : str
    phone : Optional[str]
    email : EmailStr
    created_at : datetime = Field(default_factory=datetime.utcnow)
    updated_at : datetime = Field(default_factory=datetime.utcnow)
    user : "User" = Relationship(back_populates="contacts")
    


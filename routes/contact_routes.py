from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException,status
from sqlmodel import Session, select

from config.db import get_session
from models.schema import ContactCreate, ContactUpdate, UserRole
from models.tables import Contact, User
from utils.auth_utils import get_current_user

contact_router = APIRouter()

@contact_router.post("/create")
def create_contact(contact_data:ContactCreate,current_user:User=Depends(get_current_user),session:Session=Depends(get_session)):
    try:
        if current_user.role not in [UserRole.USER,UserRole.ADMIN]:
            raise HTTPException(status_code=403, detail="Only User or Admin can create contacts")
        exist_contact = session.exec(select(Contact).where(Contact.user_id == current_user.id)).first()
        if exist_contact:
            raise HTTPException(status_code=400, detail="Contact already exists")
        new_contact = Contact(
            user_id=current_user.id,
            name=contact_data.name,
            phone=contact_data.phone,
            email=contact_data.email,
            created_at=datetime.utcnow()
        )
        session.add(new_contact)
        session.commit()
        session.refresh(new_contact)
        return {"message":"Contact is created successfully","data":new_contact}
    except Exception as e:
        return{
            "message": str(e),
            "status": "error",
            "data": None
        }
        
@contact_router.get("/all")
def get_contacts(current_user:User=Depends(get_current_user),session:Session=Depends(get_session)):
    try:
        if current_user.role == UserRole.ADMIN:
            contacts = session.exec(select(Contact)).all()
        elif current_user.role == UserRole.USER:
            contacts = session.exec(select(Contact).where(Contact.user_id==current_user.id)).all()
        else:
            raise HTTPException(status_code=403, detail="You are not allowed to view contacts.")
           
        return {"message":"Contacts retrived successflly","data":contacts}
    except Exception as e:
        return{
            "message": str(e),
            "status": "error",
            "data": None
        }
        

@contact_router.get("/{contact_id}")
def get_contact_by_id(contact_id:int,current_user:User=Depends(get_current_user),session:Session=Depends(get_session)):
    try:
        contact = session.get(Contact,contact_id)
        if not contact:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
        if current_user.role == UserRole.ADMIN:
            return {"message":"Contact retrived successfully","data":contact} 
        elif current_user.role == UserRole.USER:
            if contact.user_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You do not have permission to access this contact",
                )
            return {"message":"Contact retrived successfully","data":contact}   
        else:   
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    except Exception as e:       
        return{
            "message": str(e),
            "status": "error",
            "data": None
        }
        
@contact_router.put("/{contact_id}/update")
def update_contact(contact_id:int,contact_data:ContactUpdate,current_user:User=Depends(get_current_user),session:Session=Depends(get_session)):
    try:
        contact = session.get(Contact,contact_id)
        if not contact:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
        if current_user.role == UserRole.ADMIN:
            updated_contact = contact_data.model_dump(exclude_unset=True)
            contact.sqlmodel_update(updated_contact)
        elif current_user.role == UserRole.USER:
            if contact.user_id != current_user.id:
                raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="You do not have permission to access this contact",
                    )
            updated_contact = contact_data.model_dump(exclude_unset=True)
            contact.sqlmodel_update(updated_contact)
        else:   
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

        session.commit()
        session.refresh(contact)
        
        return {"message":"Contact is Updated successfully","data":contact}
    except Exception as e:
        return{
            "message": str(e),
            "status": "error",
            "data": None
        }
        
@contact_router.delete("/{contact_id}/cancel")
def cancel_contact(contact_id:int,current_user:User=Depends(get_current_user),session:Session=Depends(get_session)):
    try:
        contact = session.get(Contact,contact_id)
        if not contact:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
        if current_user.role == UserRole.ADMIN:
            session.delete(contact)
            session.commit()
            return {"message":"Contact is deleted successfully","data":None}
            
        elif current_user.role == UserRole.USER:
            if contact.user_id != current_user.id:
                raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="You do not have permission to access this contact",
                    )
            session.delete(contact)
            session.commit()
            return {"message":"Contact is deleted successfully","data":None}
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    except Exception as e:
        return{
            "message": str(e),
            "status": "error",
            "data": None
        }
    
        
            
        

        
    
        
            
        
    
    
        
        
        
        
        
        
        
from pydantic import BaseModel, EmailStr
from app.api.auth.models import Role
from typing import Optional

#KKKS
class KKKSBase(BaseModel):
    name : str

class CreateKKKS(KKKSBase):
    pass

class GetKKKS(KKKSBase):
    id : str
    class Config:
        from_attributes = True

#User
class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: Role

class CreateKKKSUser(UserBase):
    kkks_id: str
    password: str

class CreateAdmin(UserBase):
    password: str

class GetUser(UserBase):
    id: str

    class Config:
        from_attributes = True
        
class GetKKKSUser(UserBase):
    id: str
    kkks_id: Optional[str] = None
    
    class Config:
        from_attributes = True

class VerifyUser(GetUser):
    verfied_status: bool

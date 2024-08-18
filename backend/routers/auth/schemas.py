from pydantic import BaseModel, EmailStr
from backend.routers.auth.models import Role
from typing import Optional

#KKKS
class KKKSBase(BaseModel):
    nama_kkks : str

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
    kkks_id: Optional[str]
    role: Role

class CreateUser(UserBase):
    password: str

class GetUser(UserBase):
    id: str

    class Config:
        from_attributes = True

class VerifyUser(GetUser):
    verfied_status: bool

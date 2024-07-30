from pydantic import BaseModel, EmailStr
from app.routers.auth.models import Role

#KKKS
class KKKSBase(BaseModel):
    nama_kkks : str

class KKKSCreate(KKKSBase):
    pass

class KKKS(KKKSBase):
    id : str
    class Config:
        from_attributes = True

#User
class UserBase(BaseModel):
    username: str
    email: EmailStr
    kkks_id: str
    role: Role

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

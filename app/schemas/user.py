from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    full_name: str
    phone: str
    email: EmailStr
    password: str

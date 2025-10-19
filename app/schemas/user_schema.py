from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
import re


class UserBase(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    cpf: str = Field(..., max_length=14)
    phone: str = Field(..., max_length=20)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)
    picture_id: Optional[str] = Field(None, max_length=255)
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Valida senha forte"""
        if not re.search(r'[A-Z]', v):
            raise ValueError('Senha deve conter ao menos uma letra maiúscula')
        if not re.search(r'[a-z]', v):
            raise ValueError('Senha deve conter ao menos uma letra minúscula')
        if not re.search(r'[0-9]', v):
            raise ValueError('Senha deve conter ao menos um número')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Senha deve conter ao menos um caractere especial')
        return v


class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=2, max_length=100)
    last_name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    picture_id: Optional[str] = Field(None, max_length=255)


class UserChangePassword(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=100)
    
    @field_validator('new_password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Valida senha forte"""
        if not re.search(r'[A-Z]', v):
            raise ValueError('Senha deve conter ao menos uma letra maiúscula')
        if not re.search(r'[a-z]', v):
            raise ValueError('Senha deve conter ao menos uma letra minúscula')
        if not re.search(r'[0-9]', v):
            raise ValueError('Senha deve conter ao menos um número')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Senha deve conter ao menos um caractere especial')
        return v


class UserResponse(UserBase):
    id: int
    picture_id: Optional[str] = None
    nfc_list_id: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserListResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    picture_id: Optional[str] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
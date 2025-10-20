from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class UserPictureBase(BaseModel):
    filename: str
    file_size: int
    mime_type: str


class UserPictureResponse(UserPictureBase):
    id: int
    user_id: int
    filepath: str
    url: str
    is_active: bool
    uploaded_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class UserPictureList(BaseModel):
    id: int
    url: str
    is_active: bool
    uploaded_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
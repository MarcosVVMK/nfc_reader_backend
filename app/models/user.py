from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id          = Column(Integer, primary_key=True, index=True)
    first_name  = Column(String, index=True)
    last_name   = Column(String, index=True)
    email       = Column(String, unique=True, index=True)
    password    = Column(String, index=True)
    cpf         = Column(String, unique=True, index=True)
    phone       = Column(String, unique=True, index=True)
    picture_id  = Column(String, index=True)
    created_at  = Column(DateTime(timezone=True), server_default=func.now())
    updated_at  = Column(DateTime(timezone=True), onupdate=func.now())
    
    nfcs = relationship("Nfc", back_populates="user")
    pictures = relationship("UserPicture", back_populates="user", cascade="all, delete-orphan")
    
    @property
    def current_picture(self):
        return next((p for p in self.pictures if p.is_active), None)
    
    @property
    def profile_picture_url(self):
        picture = self.current_picture
        return picture.url if picture else None
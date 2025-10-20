from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class UserPicture(Base):
    __tablename__ = "user_pictures"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Informações do arquivo
    filename = Column(String(255), nullable=False)  # nome_original.jpg
    filepath = Column(String(500), nullable=False, unique=True)  # uploads/users/123/foto.jpg
    file_size = Column(Integer)  # tamanho em bytes
    mime_type = Column(String(50))  # image/jpeg, image/png
    
    # Controle
    is_active = Column(Boolean, default=True, index=True)  # Foto de perfil atual
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamento
    user = relationship("User", back_populates="pictures")
    
    @property
    def url(self):
        """Retorna URL pública para acessar a imagem"""
        return f"/static/uploads/users/{self.user_id}/{self.filename}"
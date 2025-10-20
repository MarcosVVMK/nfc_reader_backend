from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Nfc(Base):
    __tablename__ = "nfcs"

    id              = Column(Integer, primary_key=True, index=True)
    access_key      = Column(String(44), unique=True, index=True, nullable=False)
    nfc_number      = Column(String(20), nullable=False)
    model           = Column(String(2))
    emission_date   = Column(DateTime, nullable=False, index=True)
    emission_city   = Column(String(100), index=True)
    emission_uf     = Column(String(2), index=True)
    nfc_total_price = Column(Float, nullable=False)
    discount_value  = Column(Float, default=0.0)
    
    issuer          = relationship("Issuer", back_populates="nfcs")
    products        = relationship("ProductNfc", back_populates="nfc", cascade="all, delete-orphan")
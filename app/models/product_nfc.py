from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class ProductNfc(Base):
    __tablename__ = "products_nfc"

    id              = Column(Integer, primary_key=True, index=True)
    count_items     = Column(Integer, nullable=False)
    description     = Column(String(255), nullable=False, index=True)
    quantity        = Column(Float, nullable=False)
    unit_type       = Column(String(10), nullable=False)
    unit_value      = Column(Float, nullable=False, index=True)
    total_price     = Column(Float, nullable=False)
    price_per_unit  = Column(Float, nullable=False, index=True)
    
    nfc             = relationship("Nfc", back_populates="product")
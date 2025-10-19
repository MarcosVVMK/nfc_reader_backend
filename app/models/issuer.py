from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session

Base = declarative_base()

class Issuer(Base):
    __tablename__ = "issuers"

    id                  = Column(Integer, primary_key=True, index=True)
    cnpj                = Column(String(18), unique=True, index=True, nullable=False)
    name                = Column(String(255), nullable=False)
    fantasy_name        = Column(String(255))
    state_subscription  = Column(String(50))
    street              = Column(String(255))
    neighborhood        = Column(String(100))
    zipcode             = Column(String(10))
    city                = Column(String(100))
    uf                  = Column(String(2))
    phone               = Column(String(20))

    nfcs = relationship("Nfc", back_populates="issuer")

from datetime import datetime
from typing import Optional
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class IssuerSchema(BaseModel):
    cnpj: str
    name: str
    fantasy_name: Optional[str] = None
    state_subscription: Optional[str] = None
    address: Optional[str] = None
    neightborhood: Optional[str] = None
    zipcode: Optional[str] = None
    city: Optional[str] = None
    uf: Optional[str] = None
    phone: Optional[str] = None
    
    class Config:
        from_attributes = True


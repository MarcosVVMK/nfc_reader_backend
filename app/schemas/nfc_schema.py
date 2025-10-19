from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from app.schemas.Issuer_schema import IssuerSchema
from app.schemas.product_nfc_schema import ProductNfcCreate, ProductNfcSchema

class NfcCreate(BaseModel):
    access_key: str
    nfc_number: str
    model: Optional[str] = None
    serie: Optional[str] = None
    emission_date: datetime
    emission_city: Optional[str] = None
    emission_uf: Optional[str] = None
    nfc_total_price: float
    discount_value: float = 0.0
    issuer: IssuerSchema
    products: List[ProductNfcCreate]


class NfcSchema(BaseModel):
    id: int
    access_key: str
    nfc_number: str
    emission_date: datetime
    emission_city: Optional[str] = None
    emission_uf: Optional[str] = None
    nfc_total_price: float
    issuer: IssuerSchema
    products: List[ProductNfcSchema]
    
    class Config:
        from_attributes = True
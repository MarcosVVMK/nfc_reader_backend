from pydantic import BaseModel

class ProductNfcCreate(BaseModel):
    count_items: int
    description: str
    quantity: float
    unit_type: str
    unit_value: float
    valor_total: float
    
class ProductNfcSchema(BaseModel):
    count_items: int
    description: str
    quantity: float
    unit_type: str
    unit_value: float
    total_price: float
    price_per_unit: float
    
    class Config:
        from_attributes = True
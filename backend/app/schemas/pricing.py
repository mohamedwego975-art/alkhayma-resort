from pydantic import BaseModel
from decimal import Decimal
from typing import List, Dict, Any


class PriceBreakdownResponse(BaseModel):
    base_price: Decimal
    final_price: Decimal
    nightly_rate: Decimal
    discounts: List[Dict[str, Any]]
    multipliers: List[Dict[str, Any]]
    total_savings: Decimal
    currency: str = "USD"
    
    class Config:
        from_attributes = True

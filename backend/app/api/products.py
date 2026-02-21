from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from typing import Optional

router = APIRouter(prefix="/api/products", tags=["products"])

@router.get("/")
async def get_products(
    type: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """Get all products"""
    mock_products = [
        {
            "id": 1,
            "name": "Deluxe Sea View Room",
            "name_ar": "غرفة ديلوكس بإطلالة بحرية",
            "type": "room",
            "base_price": 1500.0,
            "capacity": 2,
            "description": "Spacious room with stunning sea view"
        },
        {
            "id": 2,
            "name": "Standard Room",
            "name_ar": "غرفة عادية",
            "type": "room",
            "base_price": 1000.0,
            "capacity": 2,
            "description": "Comfortable standard room"
        }
    ]
    
    if type:
        return [p for p in mock_products if p["type"] == type]
    return mock_products

@router.get("/{product_id}")
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    """Get product by ID"""
    return {
        "id": product_id,
        "name": "Deluxe Sea View Room",
        "type": "room",
        "base_price": 1500.0,
        "capacity": 2
    }

@router.get("/{product_id}/price")
async def get_product_price(
    product_id: int,
    check_in: str = Query(...),
    check_out: str = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Get product pricing"""
    return {"final_price": 1500.0, "base_price": 1500.0}

@router.get("/availability")
async def check_availability(
    product_id: int = Query(...),
    check_in: str = Query(...),
    check_out: str = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Check product availability"""
    return {"available": True, "remaining_capacity": 2}

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.api.auth import oauth2_scheme

router = APIRouter(prefix="/api/loyalty", tags=["loyalty"])

@router.get("/profile")
async def get_loyalty_profile(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    """Get user loyalty profile"""
    return {"points": 150, "tier": "Bronze", "lifetime_points": 150}

@router.post("/redeem")
async def redeem_points(
    redemption_data: dict,
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    """Redeem loyalty points"""
    return {"message": "Points redeemed successfully", "remaining_points": 100}

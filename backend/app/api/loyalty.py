from fastapi import APIRouter, Depends
from app.core.deps import get_current_user_optional
from app.models.user import User

router = APIRouter(prefix="/loyalty", tags=["loyalty"])


@router.get("/balance")
async def get_balance(user: User | None = Depends(get_current_user_optional)):
    """Get loyalty points balance (for frontend)."""
    if user:
        return {"points": 150, "tier": "Bronze", "lifetime_points": 150}
    return {"points": 0, "tier": "Guest", "lifetime_points": 0}


@router.get("/transactions")
async def get_transactions(user: User | None = Depends(get_current_user_optional)):
    """Get loyalty transactions (for frontend)."""
    if user:
        return {"transactions": [{"type": "earn", "points": 50, "description": "Booking"}]}
    return {"transactions": []}


@router.get("/profile")
async def get_loyalty_profile(user: User | None = Depends(get_current_user_optional)):
    """Get user loyalty profile."""
    if user:
        return {"points": 150, "tier": "Bronze", "lifetime_points": 150}
    return {"points": 0, "tier": "Guest", "lifetime_points": 0}


@router.post("/redeem")
async def redeem_points(redemption_data: dict, user: User | None = Depends(get_current_user_optional)):
    """Redeem loyalty points."""
    if not user:
        return {"message": "Login required", "remaining_points": 0}
    return {"message": "Points redeemed successfully", "remaining_points": 100}

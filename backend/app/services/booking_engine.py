from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, timedelta
from decimal import Decimal
from typing import List, Dict, Any
import httpx

from app.models import Product, Inventory, Booking, BookingItem, BookingStatus
from app.services.pricing import PricingEngine
from app.core.config import settings


class BookingEngine:
    
    @staticmethod
    async def create_booking(
        db: AsyncSession,
        user_id: int,
        product_id: int,
        check_in: date,
        check_out: date,
        quantity: int,
        idempotency_key: str,
        notes: str | None = None,
        addons: List[int] = None
    ) -> Dict[str, Any]:
        """
        Create booking with atomic inventory locking.
        Returns booking with pricing breakdown or raises exception.
        """
        
        # STEP 1: Check idempotency key
        existing = await db.execute(
            select(Booking).where(Booking.idempotency_key == idempotency_key)
        )
        if existing.scalar_one_or_none():
            raise ValueError("Duplicate idempotency key")
        
        # STEP 2: Load and validate product
        product_result = await db.execute(
            select(Product).where(Product.id == product_id)
        )
        product = product_result.scalar_one_or_none()
        
        if not product:
            raise ValueError("Product not found")
        
        if not product.is_active:
            raise ValueError("Product is not active")
        
        # Calculate nights and dates
        nights = (check_out - check_in).days
        if nights <= 0:
            raise ValueError("Check-out must be after check-in")
        
        dates_needed = [check_in + timedelta(days=i) for i in range(nights)]
        days_ahead = (check_in - date.today()).days
        
        # STEP 3-4: Lock inventory rows with SELECT FOR UPDATE NOWAIT
        inventory_query = (
            select(Inventory)
            .where(
                Inventory.product_id == product_id,
                Inventory.date.in_(dates_needed)
            )
            .order_by(Inventory.date)
            .with_for_update(nowait=True)
        )
        
        try:
            inventory_result = await db.execute(inventory_query)
            inventory_rows = inventory_result.scalars().all()
        except Exception as e:
            if "could not obtain lock" in str(e).lower():
                raise ValueError("Resource is currently being booked by another user")
            raise
        
        # STEP 5: Validate availability
        if len(inventory_rows) != len(dates_needed):
            raise ValueError("Inventory not available for all dates")
        
        for inv in inventory_rows:
            if inv.available < quantity:
                raise ValueError(f"Not enough availability for {inv.date}")
        
        # STEP 6: Calculate price
        price_breakdown = PricingEngine.calculate(
            base_price=product.base_price,
            product_type=product.type.value,
            check_in=check_in,
            nights=nights,
            days_ahead=days_ahead,
            quantity=quantity
        )
        
        # STEP 7: Create booking
        booking = Booking(
            user_id=user_id,
            idempotency_key=idempotency_key,
            status=BookingStatus.pending,
            check_in=check_in,
            check_out=check_out,
            total_price=price_breakdown.final_price,
            pricing_breakdown={
                "base_price": str(price_breakdown.base_price),
                "final_price": str(price_breakdown.final_price),
                "nightly_rate": str(price_breakdown.nightly_rate),
                "discounts": [
                    {"reason": d["reason"], "amount": str(d["amount"])}
                    for d in price_breakdown.discounts
                ],
                "multipliers": [
                    {"reason": m["reason"], "factor": str(m["factor"])}
                    for m in price_breakdown.multipliers
                ],
                "total_savings": str(price_breakdown.total_savings),
                "currency": price_breakdown.currency
            },
            notes=notes
        )
        db.add(booking)
        await db.flush()  # Get booking ID
        
        # Create booking item
        booking_item = BookingItem(
            booking_id=booking.id,
            product_id=product_id,
            quantity=quantity,
            unit_price=price_breakdown.nightly_rate,
            total_price=price_breakdown.final_price
        )
        db.add(booking_item)
        
        # STEP 8: Deduct inventory
        for inv in inventory_rows:
            inv.available -= quantity
            inv.booked += quantity
        
        # STEP 9: Commit happens in the calling function
        
        return {
            "booking_id": booking.id,
            "status": booking.status.value,
            "check_in": str(booking.check_in),
            "check_out": str(booking.check_out),
            "total_price": str(booking.total_price),
            "pricing_breakdown": booking.pricing_breakdown,
            "product": {
                "id": product.id,
                "name": product.name,
                "type": product.type.value
            }
        }
    
    @staticmethod
    async def fire_webhook(booking_data: Dict[str, Any]):
        """Fire n8n webhook asynchronously (non-blocking)"""
        webhook_url = getattr(settings, 'n8n_webhook_url', None)
        if not webhook_url:
            return
        
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                await client.post(webhook_url, json=booking_data)
        except Exception:
            # Silently fail - webhook is non-critical
            pass

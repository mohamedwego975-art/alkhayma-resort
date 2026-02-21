from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.payment import Payment, PaymentStatus

class PaymentRepository(BaseRepository[Payment]):
    def __init__(self, db: AsyncSession):
        super().__init__(Payment, db)

    async def get_by_booking(self, booking_id: int) -> List[Payment]:
        result = await self.db.execute(
            select(Payment).where(Payment.booking_id == booking_id)
        )
        return list(result.scalars().all())

    async def get_by_transaction_id(self, transaction_id: str) -> Optional[Payment]:
        result = await self.db.execute(
            select(Payment).where(Payment.transaction_id == transaction_id)
        )
        return result.scalar_one_or_none()

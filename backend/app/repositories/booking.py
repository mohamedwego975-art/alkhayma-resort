from typing import List
from datetime import date
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.booking import Booking, BookingStatus

class BookingRepository(BaseRepository[Booking]):
    def __init__(self, db: AsyncSession):
        super().__init__(Booking, db)

    async def get_by_user(self, user_id: int) -> List[Booking]:
        result = await self.db.execute(
            select(Booking).where(Booking.user_id == user_id).order_by(Booking.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_active_bookings(self, room_id: int) -> List[Booking]:
        result = await self.db.execute(
            select(Booking).where(
                and_(
                    Booking.room_id == room_id,
                    Booking.status.in_([BookingStatus.CONFIRMED, BookingStatus.CHECKED_IN])
                )
            )
        )
        return list(result.scalars().all())

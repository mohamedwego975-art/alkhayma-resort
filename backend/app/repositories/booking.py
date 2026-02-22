from typing import List, Optional
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

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Booking]:
        result = await self.db.execute(
            select(Booking).order_by(Booking.created_at.desc()).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def update_status(self, booking_id: int, status: BookingStatus) -> Optional[Booking]:
        booking = await self.get(booking_id)
        if not booking:
            return None
        booking.status = status
        await self.db.commit()
        await self.db.refresh(booking)
        return booking

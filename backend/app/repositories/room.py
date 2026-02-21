from typing import List
from datetime import date
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.room import Room, RoomStatus

class RoomRepository(BaseRepository[Room]):
    def __init__(self, db: AsyncSession):
        super().__init__(Room, db)

    async def get_available_rooms(
        self, check_in: date, check_out: date, room_type: str = None
    ) -> List[Room]:
        query = select(Room).where(Room.status == RoomStatus.AVAILABLE)
        if room_type:
            query = query.where(Room.type == room_type)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_by_number(self, room_number: str) -> Room:
        result = await self.db.execute(select(Room).where(Room.room_number == room_number))
        return result.scalar_one_or_none()

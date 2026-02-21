from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import date
from app.core.database import get_db
from app.core.exceptions import NotFoundException
from app.repositories import RoomRepository
from app.schemas.room import RoomResponse, RoomAvailabilityQuery

router = APIRouter(prefix="/rooms", tags=["rooms"])

@router.get("", response_model=List[RoomResponse])
async def get_rooms(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    repo = RoomRepository(db)
    return await repo.get_multi(skip=skip, limit=limit)

@router.get("/available", response_model=List[RoomResponse])
async def get_available_rooms(
    check_in: date,
    check_out: date,
    room_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    repo = RoomRepository(db)
    return await repo.get_available_rooms(check_in, check_out, room_type)

@router.get("/{room_id}", response_model=RoomResponse)
async def get_room(room_id: int, db: AsyncSession = Depends(get_db)):
    repo = RoomRepository(db)
    room = await repo.get(room_id)
    if not room:
        raise NotFoundException("Room", room_id)
    return room

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.exceptions import NotFoundException, ValidationException
from app.repositories import BookingRepository, RoomRepository
from app.schemas.booking import BookingCreate, BookingResponse
from app.models.user import User
from app.models.booking import BookingStatus

router = APIRouter(prefix="/bookings", tags=["bookings"])

@router.post("", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
async def create_booking(
    booking_data: BookingCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    room_repo = RoomRepository(db)
    room = await room_repo.get(booking_data.room_id)
    if not room:
        raise NotFoundException("Room", booking_data.room_id)
    
    if booking_data.check_in >= booking_data.check_out:
        raise ValidationException("Check-out must be after check-in")
    
    booking_repo = BookingRepository(db)
    booking = await booking_repo.create({
        "user_id": current_user.id,
        "room_id": booking_data.room_id,
        "check_in": booking_data.check_in,
        "check_out": booking_data.check_out,
        "guests": booking_data.guests,
        "total_price": booking_data.total_price,
        "status": BookingStatus.PENDING
    })
    
    return booking

@router.get("/my-bookings", response_model=List[BookingResponse])
async def get_my_bookings(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    repo = BookingRepository(db)
    return await repo.get_by_user(current_user.id)

@router.get("/{booking_id}", response_model=BookingResponse)
async def get_booking(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    repo = BookingRepository(db)
    booking = await repo.get(booking_id)
    if not booking:
        raise NotFoundException("Booking", booking_id)
    return booking

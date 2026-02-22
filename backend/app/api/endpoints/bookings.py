from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.core.database import get_db
from app.core.deps import get_current_user, require_role
from app.core.exceptions import NotFoundException, ValidationException
from app.repositories import BookingRepository, RoomRepository
from app.schemas.booking import BookingCreate, BookingResponse, BookingStatusUpdate
from app.models.user import User, UserRole
from app.models.booking import BookingStatus
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
async def create_booking(
    booking_data: BookingCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    room_repo = RoomRepository(db)
    room = await room_repo.get(booking_data.room_id)
    if not room:
        raise NotFoundException("Room", booking_data.room_id)

    if booking_data.check_in >= booking_data.check_out:
        raise ValidationException("Check-out must be after check-in")

    booking_repo = BookingRepository(db)
    booking = await booking_repo.create(
        {
            "user_id": current_user.id,
            "room_id": booking_data.room_id,
            "check_in": booking_data.check_in,
            "check_out": booking_data.check_out,
            "guests": booking_data.guests,
            "total_price": booking_data.total_price,
            "status": BookingStatus.PENDING,
        }
    )

    return booking


@router.get("", response_model=List[BookingResponse])
async def list_bookings(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    """List all bookings for the current user"""
    repo = BookingRepository(db)
    return await repo.get_by_user(current_user.id)


@router.get("/my-bookings", response_model=List[BookingResponse])
async def get_my_bookings(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    repo = BookingRepository(db)
    return await repo.get_by_user(current_user.id)


@router.get("/{booking_id}", response_model=BookingResponse)
async def get_booking(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = BookingRepository(db)
    booking = await repo.get(booking_id)
    if not booking:
        raise NotFoundException("Booking", booking_id)
    return booking


@router.get("/admin/all", response_model=List[BookingResponse])
async def admin_list_bookings(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    current_user: User = Depends(require_role(UserRole.ADMIN, UserRole.STAFF)),
    db: AsyncSession = Depends(get_db),
):
    """Admin: List all bookings across all users"""
    repo = BookingRepository(db)
    bookings = await repo.get_all(skip=skip, limit=limit)
    logger.info(f"Admin {current_user.email} fetched all bookings (count={len(bookings)})")
    return bookings


@router.patch("/admin/{booking_id}/status", response_model=BookingResponse)
async def admin_update_booking_status(
    booking_id: int,
    status_update: "BookingStatusUpdate",
    current_user: User = Depends(require_role(UserRole.ADMIN, UserRole.STAFF)),
    db: AsyncSession = Depends(get_db),
):
    """Admin: Update a booking's status"""
    try:
        new_status = BookingStatus(status_update.status)
    except ValueError:
        raise ValidationException(f"Invalid status: {status_update.status}")
    repo = BookingRepository(db)
    booking = await repo.update_status(booking_id, new_status)
    if not booking:
        raise NotFoundException("Booking", booking_id)
    logger.info(f"Admin {current_user.email} updated booking {booking_id} status to {new_status}")
    return booking

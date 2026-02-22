from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import date
from app.core.database import get_db
from app.core.exceptions import NotFoundException, ValidationException
from app.core.deps import require_role
from app.repositories import RoomRepository
from app.schemas.room import RoomResponse, RoomAvailabilityQuery, RoomCreate, RoomUpdate
from app.models.user import UserRole, User
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.get("", response_model=List[RoomResponse])
async def get_rooms(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    repo = RoomRepository(db)
    return await repo.get_multi(skip=skip, limit=limit)


@router.get("/available", response_model=List[RoomResponse])
async def get_available_rooms(
    check_in: date,
    check_out: date,
    room_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
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


# Admin endpoints


@router.get("/admin/all", response_model=List[RoomResponse])
async def admin_list_all_rooms(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    current_user: User = Depends(require_role(UserRole.ADMIN, UserRole.STAFF)),
    db: AsyncSession = Depends(get_db),
):
    """Admin: List all rooms with pagination"""
    repo = RoomRepository(db)
    rooms = await repo.get_multi(skip=skip, limit=limit)
    logger.info(f"Admin {current_user.email} fetched all rooms (count={len(rooms)})")
    return rooms


@router.post("/admin", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
async def admin_create_room(
    room_data: RoomCreate,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db),
):
    """Admin: Create a new room"""
    repo = RoomRepository(db)

    # Check if room number already exists
    existing_room = await repo.get_by_number(room_data.room_number)
    if existing_room:
        raise ValidationException(f"Room number {room_data.room_number} already exists")

    room = await repo.create(room_data.model_dump())
    logger.info(f"Admin {current_user.email} created room {room.id}")
    return room


@router.patch("/admin/{room_id}", response_model=RoomResponse)
async def admin_update_room(
    room_id: int,
    room_data: RoomUpdate,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db),
):
    """Admin: Update room details"""
    repo = RoomRepository(db)
    room = await repo.get(room_id)
    if not room:
        raise NotFoundException("Room", room_id)

    # Check if new room number is not already taken
    if room_data.room_number and room_data.room_number != room.room_number:
        existing_room = await repo.get_by_number(room_data.room_number)
        if existing_room:
            raise ValidationException(
                f"Room number {room_data.room_number} already exists"
            )

    update_data = {k: v for k, v in room_data.model_dump().items() if v is not None}
    updated_room = await repo.update(room_id, update_data)
    logger.info(f"Admin {current_user.email} updated room {room_id}")
    return updated_room


@router.delete("/admin/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def admin_delete_room(
    room_id: int,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db),
):
    """Admin: Delete a room"""
    repo = RoomRepository(db)
    room = await repo.get(room_id)
    if not room:
        raise NotFoundException("Room", room_id)

    deleted = await repo.delete(room_id)
    if not deleted:
        raise NotFoundException("Room", room_id)
    logger.info(f"Admin {current_user.email} deleted room {room_id}")
    return None


@router.patch("/admin/{room_id}/status", response_model=RoomResponse)
async def admin_update_room_status(
    room_id: int,
    status_data: dict,
    current_user: User = Depends(require_role(UserRole.ADMIN, UserRole.STAFF)),
    db: AsyncSession = Depends(get_db),
):
    """Admin: Update room status (available, occupied, maintenance)"""
    repo = RoomRepository(db)
    room = await repo.get(room_id)
    if not room:
        raise NotFoundException("Room", room_id)

    new_status = status_data.get("status")
    if not new_status:
        raise ValidationException("Status is required")

    if new_status not in ["available", "occupied", "maintenance"]:
        raise ValidationException(f"Invalid status: {new_status}")

    updated_room = await repo.update(room_id, {"status": new_status})
    logger.info(
        f"Admin {current_user.email} updated room {room_id} status to {new_status}"
    )
    return updated_room


@router.patch("/admin/{room_id}/active", response_model=RoomResponse)
async def admin_toggle_room_active(
    room_id: int,
    active_data: dict,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db),
):
    """Admin: Toggle room active/inactive status"""
    repo = RoomRepository(db)
    room = await repo.get(room_id)
    if not room:
        raise NotFoundException("Room", room_id)

    is_active = active_data.get("is_active")
    if is_active is None:
        raise ValidationException("is_active status is required")

    updated_room = await repo.update(room_id, {"is_active": is_active})
    logger.info(
        f"Admin {current_user.email} toggled room {room_id} active status to {is_active}"
    )
    return updated_room

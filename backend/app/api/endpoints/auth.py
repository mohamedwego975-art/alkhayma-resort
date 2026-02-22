from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.schemas.auth import UserLogin, UserRegister, Token, UserResponse
from app.core.security import create_access_token, verify_password, get_password_hash
from app.core.deps import get_current_user, require_role
from app.core.exceptions import (
    AlreadyExistsException,
    UnauthorizedException,
    NotFoundException,
    ValidationException,
)
from app.repositories import UserRepository
from app.models.user import User, UserRole
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register(user_data: UserRegister, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)

    if await repo.get_by_email(user_data.email):
        raise AlreadyExistsException("User", "email", user_data.email)

    if user_data.phone and await repo.get_by_phone(user_data.phone):
        raise AlreadyExistsException("User", "phone", user_data.phone)

    user = await repo.create(
        {
            "email": user_data.email,
            "phone": user_data.phone,
            "full_name": user_data.full_name,
            "hashed_password": get_password_hash(user_data.password),
            "role": UserRole.GUEST,
        }
    )

    return user


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    user = await repo.get_by_email(credentials.email)

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise UnauthorizedException("Invalid email or password")

    if not user.is_active:
        raise UnauthorizedException("Account is inactive")

    access_token = create_access_token({"sub": str(user.id), "role": user.role.value})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    return {"message": "Logged out successfully"}


@router.get("/admin/users", response_model=List[UserResponse])
async def admin_list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db),
):
    """Admin: List all registered users"""
    repo = UserRepository(db)
    users = await repo.get_all(skip=skip, limit=limit)
    logger.info(f"Admin {current_user.email} fetched all users (count={len(users)})")
    return users


@router.patch("/admin/users/{user_id}", response_model=UserResponse)
async def admin_update_user(
    user_id: int,
    user_data: dict,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db),
):
    """Admin: Update user information"""
    repo = UserRepository(db)
    user = await repo.get(user_id)
    if not user:
        raise NotFoundException("User", user_id)

    # Don't allow changing critical fields without validation
    allowed_fields = {"full_name", "phone", "role"}
    update_data = {
        k: v for k, v in user_data.items() if k in allowed_fields and v is not None
    }

    if not update_data:
        raise ValidationException("No valid fields to update")

    updated_user = await repo.update(user_id, update_data)
    logger.info(f"Admin {current_user.email} updated user {user_id}")
    return updated_user


@router.patch("/admin/users/{user_id}/active", response_model=UserResponse)
async def admin_toggle_user_active(
    user_id: int,
    active_data: dict,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db),
):
    """Admin: Activate/Deactivate user account"""
    repo = UserRepository(db)
    user = await repo.get(user_id)
    if not user:
        raise NotFoundException("User", user_id)

    is_active = active_data.get("is_active")
    if is_active is None:
        raise ValidationException("is_active status is required")

    updated_user = await repo.update(user_id, {"is_active": is_active})
    logger.info(
        f"Admin {current_user.email} toggled user {user_id} active status to {is_active}"
    )
    return updated_user


@router.delete("/admin/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def admin_delete_user(
    user_id: int,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db),
):
    """Admin: Delete a user account"""
    repo = UserRepository(db)
    user = await repo.get(user_id)
    if not user:
        raise NotFoundException("User", user_id)

    # Prevent deleting the admin user itself
    if user_id == current_user.id:
        raise ValidationException("Cannot delete your own admin account")

    deleted = await repo.delete(user_id)
    if not deleted:
        raise NotFoundException("User", user_id)
    logger.info(f"Admin {current_user.email} deleted user {user_id}")
    return None

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.schemas.auth import UserLogin, UserRegister, Token, UserResponse
from app.core.security import create_access_token, verify_password, get_password_hash
from app.core.deps import get_current_user
from app.core.exceptions import AlreadyExistsException, UnauthorizedException
from app.repositories import UserRepository
from app.models.user import User, UserRole

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, db: AsyncSession = Depends(get_db)):
    repo = UserRepository(db)
    
    if await repo.get_by_email(user_data.email):
        raise AlreadyExistsException("User", "email", user_data.email)
    
    if user_data.phone and await repo.get_by_phone(user_data.phone):
        raise AlreadyExistsException("User", "phone", user_data.phone)
    
    user = await repo.create({
        "email": user_data.email,
        "phone": user_data.phone,
        "full_name": user_data.full_name,
        "hashed_password": get_password_hash(user_data.password),
        "role": UserRole.GUEST
    })
    
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

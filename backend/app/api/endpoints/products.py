from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.core.database import get_db
from app.core.deps import get_current_user, require_role
from app.core.exceptions import NotFoundException
from app.repositories import ProductRepository
from app.schemas.product import ProductResponse, ProductCreate
from app.models.user import User, UserRole

router = APIRouter(prefix="/products", tags=["products"])

@router.get("", response_model=List[ProductResponse])
async def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    product_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    repo = ProductRepository(db)
    if product_type:
        return await repo.get_active_products(product_type)
    return await repo.get_multi(skip=skip, limit=limit)

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    repo = ProductRepository(db)
    product = await repo.get(product_id)
    if not product:
        raise NotFoundException("Product", product_id)
    return product

@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    current_user: User = Depends(require_role(UserRole.ADMIN, UserRole.STAFF)),
    db: AsyncSession = Depends(get_db)
):
    repo = ProductRepository(db)
    product = await repo.create(product_data.model_dump())
    return product

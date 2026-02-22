from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.core.database import get_db
from app.core.deps import get_current_user, require_role
from app.core.exceptions import NotFoundException, ValidationException
from app.repositories import ProductRepository
from app.schemas.product import ProductResponse, ProductCreate, ProductUpdate
from app.models.user import User, UserRole
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=List[ProductResponse])
async def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    product_type: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    repo = ProductRepository(db)
    if product_type:
        return await repo.get_active_products(product_type)
    return await repo.get_multi(skip=skip, limit=limit)


@router.get("/home", response_model=dict)
async def get_home_products(db: AsyncSession = Depends(get_db)):
    """Get featured products for home page"""
    repo = ProductRepository(db)
    try:
        # Get featured/active products
        products = await repo.get_multi(skip=0, limit=3)
        # Transform into packages format for home page (Product uses base_price)
        packages = [
            {
                "id": p.id,
                "name": p.name,
                "description": p.description or "",
                "price": float(p.base_price) if p.base_price else 0,
                "savings": int(float(p.base_price) * 0.15) if p.base_price else 0,  # 15% savings
            }
            for p in products
        ]
        return {"packages": packages}
    except Exception as e:
        logger.error(f"Error fetching home products: {e}")
        return {
            "packages": [
                {
                    "id": 1,
                    "name": "Weekend Getaway",
                    "description": "2 nights + breakfast",
                    "price": 299,
                    "savings": 50,
                },
                {
                    "id": 2,
                    "name": "Family Package",
                    "description": "3 nights + all meals",
                    "price": 599,
                    "savings": 100,
                },
                {
                    "id": 3,
                    "name": "Luxury Escape",
                    "description": "5 nights + VIP beach",
                    "price": 999,
                    "savings": 200,
                },
            ]
        }


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
    db: AsyncSession = Depends(get_db),
):
    repo = ProductRepository(db)
    product = await repo.create(product_data.model_dump())
    logger.info(f"Admin {current_user.email} created product {product.id}")
    return product


# Admin endpoints


@router.get("/admin/all", response_model=List[ProductResponse])
async def admin_list_all_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=200),
    current_user: User = Depends(require_role(UserRole.ADMIN, UserRole.STAFF)),
    db: AsyncSession = Depends(get_db),
):
    """Admin: List all products with pagination"""
    repo = ProductRepository(db)
    products = await repo.get_multi(skip=skip, limit=limit)
    logger.info(
        f"Admin {current_user.email} fetched all products (count={len(products)})"
    )
    return products


@router.post(
    "/admin", response_model=ProductResponse, status_code=status.HTTP_201_CREATED
)
async def admin_create_product(
    product_data: ProductCreate,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db),
):
    """Admin: Create a new product"""
    repo = ProductRepository(db)
    product = await repo.create(product_data.model_dump())
    logger.info(f"Admin {current_user.email} created product {product.id}")
    return product


@router.patch("/admin/{product_id}", response_model=ProductResponse)
async def admin_update_product(
    product_id: int,
    product_data: ProductUpdate,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db),
):
    """Admin: Update product details"""
    repo = ProductRepository(db)
    product = await repo.get(product_id)
    if not product:
        raise NotFoundException("Product", product_id)

    update_data = {k: v for k, v in product_data.model_dump().items() if v is not None}
    if not update_data:
        raise ValidationException("No valid fields to update")

    updated_product = await repo.update(product_id, update_data)
    logger.info(f"Admin {current_user.email} updated product {product_id}")
    return updated_product


@router.delete("/admin/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def admin_delete_product(
    product_id: int,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db),
):
    """Admin: Delete a product"""
    repo = ProductRepository(db)
    product = await repo.get(product_id)
    if not product:
        raise NotFoundException("Product", product_id)

    deleted = await repo.delete(product_id)
    if not deleted:
        raise NotFoundException("Product", product_id)
    logger.info(f"Admin {current_user.email} deleted product {product_id}")
    return None


@router.patch("/admin/{product_id}/active", response_model=ProductResponse)
async def admin_toggle_product_active(
    product_id: int,
    active_data: dict,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db),
):
    """Admin: Toggle product active/inactive status"""
    repo = ProductRepository(db)
    product = await repo.get(product_id)
    if not product:
        raise NotFoundException("Product", product_id)

    is_active = active_data.get("is_active")
    if is_active is None:
        raise ValidationException("is_active status is required")

    updated_product = await repo.update(product_id, {"is_active": is_active})
    logger.info(
        f"Admin {current_user.email} toggled product {product_id} active status to {is_active}"
    )
    return updated_product

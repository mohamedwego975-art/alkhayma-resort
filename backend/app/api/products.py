from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from decimal import Decimal
from typing import Optional
import json
import math

from app.core.database import get_db
from app.core.redis import redis_client, invalidate_pattern
from app.models import Product, ProductType, Package, Inventory
from app.services.pricing import PricingEngine
from app.schemas.product import (
    ProductResponse,
    ProductDetailResponse,
    PackageResponse,
    HomeResponse,
    PaginatedProductsResponse,
    PriceBreakdownResponse
)

router = APIRouter(prefix="/api/products", tags=["Products"])


@router.get("/home", response_model=HomeResponse)
async def get_home_featured(db: AsyncSession = Depends(get_db)):
    """
    Get featured content for home page.
    Cached in Redis for 10 minutes.
    """
    
    # Check cache
    cache_key = "home:featured"
    cached = await redis_client.get(cache_key)
    if cached:
        cached_data = json.loads(cached)
        return HomeResponse(**cached_data)
    
    # Get featured rooms (3)
    rooms_result = await db.execute(
        select(Product)
        .where(Product.type == ProductType.room, Product.is_active == True)
        .order_by(Product.sort_order, Product.id)
        .limit(3)
    )
    featured_rooms = rooms_result.scalars().all()
    
    # Get packages (4)
    packages_result = await db.execute(
        select(Package)
        .where(Package.is_active == True)
        .limit(4)
    )
    packages = packages_result.scalars().all()
    
    # Get activities teaser (3) - water activities + events
    activities_result = await db.execute(
        select(Product)
        .where(
            Product.type.in_([ProductType.water_activity, ProductType.event]),
            Product.is_active == True
        )
        .order_by(Product.sort_order, Product.id)
        .limit(3)
    )
    activities = activities_result.scalars().all()
    
    response_data = {
        "featured_rooms": [ProductResponse.model_validate(r).model_dump() for r in featured_rooms],
        "packages": [PackageResponse.model_validate(p).model_dump() for p in packages],
        "activities_teaser": [ProductResponse.model_validate(a).model_dump() for a in activities]
    }
    
    # Cache for 10 minutes
    await redis_client.setex(
        cache_key,
        600,
        json.dumps(response_data, default=str)
    )
    
    return HomeResponse(**response_data)


@router.get("", response_model=PaginatedProductsResponse)
async def list_products(
    type: Optional[str] = Query(None, description="Filter by product type"),
    is_active: bool = Query(True, description="Filter by active status"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    db: AsyncSession = Depends(get_db)
):
    """
    List products with filtering and pagination.
    Cached in Redis for 5 minutes.
    """
    
    # Check cache
    cache_key = f"products:{type or 'all'}:p{page}:l{limit}:a{is_active}"
    cached = await redis_client.get(cache_key)
    if cached:
        cached_data = json.loads(cached)
        return PaginatedProductsResponse(**cached_data)
    
    # Build query
    query = select(Product).where(Product.is_active == is_active)
    
    if type:
        try:
            product_type = ProductType[type]
            query = query.where(Product.type == product_type)
        except KeyError:
            raise HTTPException(status_code=400, detail=f"Invalid product type: {type}")
    
    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # Apply pagination and sorting
    query = query.order_by(Product.sort_order, Product.id)
    query = query.offset((page - 1) * limit).limit(limit)
    
    result = await db.execute(query)
    products = result.scalars().all()
    
    pages = math.ceil(total / limit) if total > 0 else 0
    
    response_data = {
        "items": [ProductResponse.model_validate(p).model_dump() for p in products],
        "total": total,
        "page": page,
        "limit": limit,
        "pages": pages
    }
    
    # Cache for 5 minutes
    await redis_client.setex(
        cache_key,
        300,
        json.dumps(response_data, default=str)
    )
    
    return PaginatedProductsResponse(**response_data)


@router.get("/{slug}", response_model=ProductDetailResponse)
async def get_product_by_slug(
    slug: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get full product details by slug.
    Includes inventory status, average rating, and review count.
    """
    
    # Get product
    result = await db.execute(
        select(Product).where(Product.slug == slug)
    )
    product = result.scalar_one_or_none()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check inventory status (check next 30 days)
    today = date.today()
    inventory_result = await db.execute(
        select(Inventory)
        .where(
            Inventory.product_id == product.id,
            Inventory.date >= today,
            Inventory.available > 0
        )
        .limit(1)
    )
    has_availability = inventory_result.scalar_one_or_none() is not None
    inventory_status = "available" if has_availability else "soldout"
    
    # TODO: Calculate average rating and review count from reviews table
    # For now, return placeholder values
    average_rating = None
    review_count = 0
    
    product_dict = ProductResponse.model_validate(product).model_dump()
    product_dict["inventory_status"] = inventory_status
    product_dict["average_rating"] = average_rating
    product_dict["review_count"] = review_count
    
    return ProductDetailResponse(**product_dict)


@router.get("/{product_id}/price", response_model=PriceBreakdownResponse)
async def get_product_price(
    product_id: int,
    check_in: date = Query(..., description="Check-in date"),
    check_out: date = Query(..., description="Check-out date"),
    quantity: int = Query(1, ge=1, description="Quantity"),
    db: AsyncSession = Depends(get_db)
):
    """
    Calculate product price with dynamic pricing rules.
    Cached in Redis for 5 minutes.
    """
    
    # Calculate nights
    nights = (check_out - check_in).days
    if nights <= 0:
        raise HTTPException(status_code=400, detail="Check-out must be after check-in")
    
    # Calculate days ahead
    days_ahead = (check_in - date.today()).days
    if days_ahead < 0:
        raise HTTPException(status_code=400, detail="Check-in date must be in the future")
    
    # Check cache
    cache_key = f"price:{product_id}:{check_in}:{check_out}:{quantity}"
    cached = await redis_client.get(cache_key)
    if cached:
        cached_data = json.loads(cached)
        # Convert string decimals back to Decimal
        cached_data["base_price"] = Decimal(cached_data["base_price"])
        cached_data["final_price"] = Decimal(cached_data["final_price"])
        cached_data["nightly_rate"] = Decimal(cached_data["nightly_rate"])
        cached_data["total_savings"] = Decimal(cached_data["total_savings"])
        for discount in cached_data["discounts"]:
            discount["amount"] = Decimal(str(discount["amount"]))
        for multiplier in cached_data["multipliers"]:
            multiplier["factor"] = Decimal(str(multiplier["factor"]))
        return PriceBreakdownResponse(**cached_data)
    
    # Get product
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if not product.is_active:
        raise HTTPException(status_code=400, detail="Product is not available")
    
    # Calculate price
    price_breakdown = PricingEngine.calculate(
        base_price=product.base_price,
        product_type=product.type.value,
        check_in=check_in,
        nights=nights,
        days_ahead=days_ahead,
        quantity=quantity
    )
    
    # Cache result (convert Decimal to string for JSON)
    cache_data = {
        "base_price": str(price_breakdown.base_price),
        "final_price": str(price_breakdown.final_price),
        "nightly_rate": str(price_breakdown.nightly_rate),
        "discounts": [
            {"reason": d["reason"], "amount": str(d["amount"])}
            for d in price_breakdown.discounts
        ],
        "multipliers": [
            {"reason": m["reason"], "factor": str(m["factor"])}
            for m in price_breakdown.multipliers
        ],
        "total_savings": str(price_breakdown.total_savings),
        "currency": price_breakdown.currency
    }
    await redis_client.setex(cache_key, 300, json.dumps(cache_data))
    
    return price_breakdown


async def invalidate_product_caches():
    """Invalidate all product-related caches"""
    await invalidate_pattern("home:*")
    await invalidate_pattern("products:*")
    await invalidate_pattern("price:*")

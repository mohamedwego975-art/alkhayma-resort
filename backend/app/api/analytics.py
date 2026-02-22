"""Analytics API endpoints for admin dashboard.

Provides revenue, occupancy, and business metrics for resort management.
"""

from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select, and_, extract
from sqlalchemy.ext.asyncio import AsyncSession
from structlog import get_logger

from app.core.deps import get_db, require_admin
from app.core.exceptions import AppException
from app.models.booking import Booking, BookingStatus
from app.models.payment import Payment, PaymentStatus
from app.models.product import Product
from app.models.room import Room, RoomStatus
from app.models.user import User
from app.schemas.analytics import (
    RevenueMetrics,
    OccupancyMetrics,
    PopularProducts,
    DashboardSummary,
    TimeRangeQuery,
)

router = APIRouter(prefix="/api/analytics", tags=["analytics"])
logger = get_logger()


@router.get("/revenue", response_model=RevenueMetrics)
async def get_revenue_metrics(
    days: int = Query(default=30, ge=1, le=365),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """Get revenue metrics for specified time period.
    
    Args:
        days: Number of days to look back (default 30)
        db: Database session
        current_user: Admin user
        
    Returns:
        RevenueMetrics with total, by-day, and by-product breakdown
    """
    try:
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Total revenue from completed payments
        total_query = select(
            func.sum(Payment.amount).label("total")
        ).where(
            and_(
                Payment.status == PaymentStatus.COMPLETED,
                Payment.created_at >= start_date
            )
        )
        total_result = await db.execute(total_query)
        total_revenue = total_result.scalar() or 0.0
        
        # Revenue by day
        daily_query = select(
            func.date(Payment.created_at).label("date"),
            func.sum(Payment.amount).label("revenue")
        ).where(
            and_(
                Payment.status == PaymentStatus.COMPLETED,
                Payment.created_at >= start_date
            )
        ).group_by(
            func.date(Payment.created_at)
        ).order_by(
            func.date(Payment.created_at)
        )
        daily_result = await db.execute(daily_query)
        daily_revenue = [
            {"date": str(row.date), "revenue": float(row.revenue)}
            for row in daily_result.fetchall()
        ]
        
        # Payment method breakdown
        method_query = select(
            Payment.method.label("method"),
            func.count(Payment.id).label("count"),
            func.sum(Payment.amount).label("total")
        ).where(
            and_(
                Payment.status == PaymentStatus.COMPLETED,
                Payment.created_at >= start_date
            )
        ).group_by(Payment.method)
        method_result = await db.execute(method_query)
        by_method = [
            {
                "method": row.method.value,
                "count": row.count,
                "total": float(row.total)
            }
            for row in method_result.fetchall()
        ]
        
        logger.info(
            "Revenue metrics fetched",
            days=days,
            total_revenue=total_revenue,
            admin_id=current_user.id
        )
        
        return RevenueMetrics(
            total=float(total_revenue),
            daily_breakdown=daily_revenue,
            by_payment_method=by_method,
            period_days=days
        )
        
    except Exception as e:
        logger.error("Failed to fetch revenue metrics", error=str(e))
        raise AppException(
            message="Failed to fetch revenue metrics",
            code="ANALYTICS_ERROR"
        )


@router.get("/occupancy", response_model=OccupancyMetrics)
async def get_occupancy_metrics(
    days: int = Query(default=30, ge=1, le=365),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """Get room occupancy metrics for specified time period.
    
    Args:
        days: Number of days to look back
        db: Database session
        current_user: Admin user
        
    Returns:
        OccupancyMetrics with rate, by-room-type, and availability
    """
    try:
        # Total rooms count
        total_rooms_query = select(func.count(Room.id)).where(Room.is_active == True)
        total_rooms_result = await db.execute(total_rooms_query)
        total_rooms = total_rooms_result.scalar() or 0
        
        # Currently occupied rooms
        occupied_query = select(func.count(Room.id)).where(
            and_(Room.is_active == True, Room.status == RoomStatus.OCCUPIED)
        )
        occupied_result = await db.execute(occupied_query)
        occupied = occupied_result.scalar() or 0
        
        # Available rooms
        available = total_rooms - occupied
        occupancy_rate = (occupied / total_rooms * 100) if total_rooms > 0 else 0.0
        
        # Occupancy by room type
        by_type_query = select(
            Room.room_type.label("room_type"),
            func.count(Room.id).label("total"),
            func.sum(
                func.case((Room.status == RoomStatus.OCCUPIED, 1), else_=0)
            ).label("occupied")
        ).where(Room.is_active == True).group_by(Room.room_type)
        by_type_result = await db.execute(by_type_query)
        by_type = [
            {
                "room_type": row.room_type.value,
                "total": row.total,
                "occupied": row.occupied or 0,
                "available": row.total - (row.occupied or 0),
                "rate": round((row.occupied or 0) / row.total * 100, 1)
            }
            for row in by_type_result.fetchall()
        ]
        
        # Recent bookings count
        start_date = datetime.utcnow() - timedelta(days=days)
        bookings_query = select(func.count(Booking.id)).where(
            Booking.created_at >= start_date
        )
        bookings_result = await db.execute(bookings_query)
        recent_bookings = bookings_result.scalar() or 0
        
        logger.info(
            "Occupancy metrics fetched",
            total_rooms=total_rooms,
            occupied=occupied,
            occupancy_rate=occupancy_rate,
            admin_id=current_user.id
        )
        
        return OccupancyMetrics(
            total_rooms=total_rooms,
            occupied=occupied,
            available=available,
            occupancy_rate=round(occupancy_rate, 1),
            by_room_type=by_type,
            recent_bookings=recent_bookings,
            period_days=days
        )
        
    except Exception as e:
        logger.error("Failed to fetch occupancy metrics", error=str(e))
        raise AppException(
            message="Failed to fetch occupancy metrics",
            code="ANALYTICS_ERROR"
        )


@router.get("/popular-products", response_model=PopularProducts)
async def get_popular_products(
    limit: int = Query(default=10, ge=1, le=50),
    days: int = Query(default=30, ge=1, le=365),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """Get most popular products by booking count.
    
    Args:
        limit: Number of top products to return
        days: Number of days to look back
        db: Database session
        current_user: Admin user
        
    Returns:
        PopularProducts list with booking counts and revenue
    """
    try:
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Product popularity query (requires booking_items table or product reference in bookings)
        # For now, simplified query based on products table
        products_query = select(
            Product.id,
            Product.name,
            Product.name_ar,
            Product.type,
            Product.base_price,
            Product.is_active
        ).where(Product.is_active == True).limit(limit)
        
        products_result = await db.execute(products_query)
        products = [
            {
                "id": row.id,
                "name": row.name,
                "name_ar": row.name_ar,
                "type": row.type.value,
                "price": float(row.base_price),
                "is_active": row.is_active,
                # Placeholder - would need booking_items for actual stats
                "booking_count": 0,
                "revenue": 0.0
            }
            for row in products_result.fetchall()
        ]
        
        logger.info(
            "Popular products fetched",
            count=len(products),
            limit=limit,
            admin_id=current_user.id
        )
        
        return PopularProducts(
            products=products,
            period_days=days,
            total_count=len(products)
        )
        
    except Exception as e:
        logger.error("Failed to fetch popular products", error=str(e))
        raise AppException(
            message="Failed to fetch popular products",
            code="ANALYTICS_ERROR"
        )


@router.get("/dashboard", response_model=DashboardSummary)
async def get_dashboard_summary(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """Get comprehensive dashboard summary for admin.
    
    Returns:
        DashboardSummary with all key metrics
    """
    try:
        today = datetime.utcnow()
        today_start = today.replace(hour=0, minute=0, second=0, microsecond=0)
        month_start = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        # Today's revenue
        today_revenue_query = select(
            func.sum(Payment.amount)
        ).where(
            and_(
                Payment.status == PaymentStatus.COMPLETED,
                Payment.created_at >= today_start
            )
        )
        today_revenue_result = await db.execute(today_revenue_query)
        today_revenue = today_revenue_result.scalar() or 0.0
        
        # Monthly revenue
        month_revenue_query = select(
            func.sum(Payment.amount)
        ).where(
            and_(
                Payment.status == PaymentStatus.COMPLETED,
                Payment.created_at >= month_start
            )
        )
        month_revenue_result = await db.execute(month_revenue_query)
        month_revenue = month_revenue_result.scalar() or 0.0
        
        # Active bookings count
        active_bookings_query = select(func.count(Booking.id)).where(
            Booking.status.in_([BookingStatus.PENDING, BookingStatus.CONFIRMED])
        )
        active_bookings_result = await db.execute(active_bookings_query)
        active_bookings = active_bookings_result.scalar() or 0
        
        # Total customers
        total_customers_query = select(func.count(User.id)).where(
            User.role == "guest"
        )
        total_customers_result = await db.execute(total_customers_query)
        total_customers = total_customers_result.scalar() or 0
        
        # Occupancy rate
        total_rooms_query = select(func.count(Room.id)).where(Room.is_active == True)
        total_rooms_result = await db.execute(total_rooms_query)
        total_rooms = total_rooms_result.scalar() or 0
        
        occupied_rooms_query = select(func.count(Room.id)).where(
            and_(Room.is_active == True, Room.status == RoomStatus.OCCUPIED)
        )
        occupied_rooms_result = await db.execute(occupied_rooms_query)
        occupied_rooms = occupied_rooms_result.scalar() or 0
        
        occupancy_rate = (occupied_rooms / total_rooms * 100) if total_rooms > 0 else 0.0
        
        logger.info(
            "Dashboard summary fetched",
            today_revenue=today_revenue,
            month_revenue=month_revenue,
            active_bookings=active_bookings,
            admin_id=current_user.id
        )
        
        return DashboardSummary(
            today_revenue=float(today_revenue),
            month_revenue=float(month_revenue),
            active_bookings=active_bookings,
            total_customers=total_customers,
            occupancy_rate=round(occupancy_rate, 1),
            occupied_rooms=occupied_rooms,
            available_rooms=total_rooms - occupied_rooms,
            last_updated=today.isoformat()
        )
        
    except Exception as e:
        logger.error("Failed to fetch dashboard summary", error=str(e))
        raise AppException(
            message="Failed to fetch dashboard summary",
            code="ANALYTICS_ERROR"
        )

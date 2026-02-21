from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models import User
from app.services.booking_engine import BookingEngine
from app.schemas.booking import CreateBookingRequest, BookingResponse

router = APIRouter(prefix="/api/bookings", tags=["Bookings"])


@router.post("", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
async def create_booking(
    booking_request: CreateBookingRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new booking with atomic inventory locking.
    Prevents overbooking and double submission.
    """
    
    try:
        booking_data = await BookingEngine.create_booking(
            db=db,
            user_id=current_user.id,
            product_id=booking_request.product_id,
            check_in=booking_request.check_in,
            check_out=booking_request.check_out,
            quantity=booking_request.quantity,
            idempotency_key=booking_request.idempotency_key,
            notes=booking_request.notes,
            addons=booking_request.addons
        )
        
        await db.commit()
        
        # Fire webhook in background (non-blocking)
        background_tasks.add_task(BookingEngine.fire_webhook, booking_data)
        
        return BookingResponse(**booking_data)
    
    except ValueError as e:
        await db.rollback()
        error_msg = str(e)
        
        # Map errors to appropriate status codes
        if "Duplicate idempotency key" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=error_msg
            )
        elif "not found" in error_msg.lower() or "not active" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=error_msg
            )
        elif "not enough availability" in error_msg.lower() or "being booked" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=error_msg
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )
    
    except Exception as e:
        await db.rollback()
        import traceback
        print(f"BOOKING ERROR: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Booking failed, rolled back, please retry"
        )

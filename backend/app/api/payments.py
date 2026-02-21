from fastapi import APIRouter, Depends, HTTPException, status, Request, BackgroundTasks
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.deps import get_current_user, require_role
from app.models import User, UserRole, Booking, BookingStatus, Payment, PaymentWebhookLog, PaymentGateway, PaymentStatus
from app.schemas.payment import InitiatePaymentRequest, PaymentResponse, PaymobPaymentResponse, StripePaymentResponse
from app.services.payment_gateway import PaymobGateway, StripeGateway
from app.services.booking_engine import BookingEngine
import json

router = APIRouter(prefix="/api/payments", tags=["Payments"])


@router.post("/initiate/{booking_id}", response_model=PaymentResponse, status_code=201)
async def initiate_payment(
    booking_id: int,
    payment_request: InitiatePaymentRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Initiate payment for a booking"""
    
    result = await db.execute(
        select(Booking).where(Booking.id == booking_id, Booking.user_id == current_user.id)
    )
    booking = result.scalar_one_or_none()
    
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    if booking.status != BookingStatus.pending:
        raise HTTPException(status_code=400, detail="Booking is not in pending status")
    
    existing_payment = await db.execute(
        select(Payment).where(Payment.booking_id == booking_id)
    )
    if existing_payment.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Payment already initiated for this booking")
    
    user_data = {
        "email": current_user.email,
        "first_name": current_user.full_name.split()[0] if current_user.full_name else "Customer",
        "last_name": current_user.full_name.split()[-1] if len(current_user.full_name.split()) > 1 else "User",
        "phone": current_user.phone or "+201000000000"
    }
    
    payment_data = {}
    paymob_data = None
    stripe_data = None
    
    if payment_request.gateway == "paymob":
        gateway_response = await PaymobGateway.initiate_payment(
            amount=booking.total_price,
            currency=payment_request.currency,
            booking_id=booking_id,
            user_data=user_data
        )
        payment_data = gateway_response
        paymob_data = PaymobPaymentResponse(**gateway_response)
        gateway_order_id = gateway_response["order_id"]
        gateway_payment_id = gateway_response["payment_key"]
        
    elif payment_request.gateway == "stripe":
        gateway_response = await StripeGateway.initiate_payment(
            amount=booking.total_price,
            currency=payment_request.currency,
            booking_id=booking_id,
            user_data=user_data
        )
        payment_data = gateway_response
        stripe_data = StripePaymentResponse(**gateway_response)
        gateway_order_id = None
        gateway_payment_id = gateway_response["payment_intent_id"]
    
    payment = Payment(
        booking_id=booking_id,
        gateway=PaymentGateway[payment_request.gateway],
        status=PaymentStatus.pending,
        amount=booking.total_price,
        currency=payment_request.currency,
        gateway_order_id=gateway_order_id,
        gateway_payment_id=gateway_payment_id,
        payment_data=payment_data
    )
    
    db.add(payment)
    await db.commit()
    await db.refresh(payment)
    
    return PaymentResponse(
        payment_id=payment.id,
        gateway=payment_request.gateway,
        amount=str(booking.total_price),
        currency=payment_request.currency,
        paymob_data=paymob_data,
        stripe_data=stripe_data
    )


@router.post("/webhook/paymob")
async def paymob_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """Handle Paymob webhook"""
    
    payload = await request.json()
    signature = payload.get("hmac", "")
    
    webhook_log = PaymentWebhookLog(
        gateway=PaymentGateway.paymob,
        payload=payload,
        signature=signature,
        is_valid=False,
        processed=False
    )
    db.add(webhook_log)
    
    is_valid = PaymobGateway.verify_webhook(payload, signature)
    webhook_log.is_valid = is_valid
    
    if not is_valid:
        await db.commit()
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    try:
        order_id = payload.get("order", {}).get("merchant_order_id")
        success = payload.get("success", False)
        
        if order_id:
            result = await db.execute(
                select(Payment).where(Payment.booking_id == int(order_id))
            )
            payment = result.scalar_one_or_none()
            
            if payment:
                if success:
                    payment.status = PaymentStatus.success
                    payment.gateway_payment_id = str(payload.get("id"))
                    
                    booking_result = await db.execute(
                        select(Booking).where(Booking.id == payment.booking_id)
                    )
                    booking = booking_result.scalar_one()
                    booking.status = BookingStatus.confirmed
                    
                    background_tasks.add_task(
                        BookingEngine.fire_webhook,
                        {"booking_id": booking.id, "status": "confirmed"}
                    )
                else:
                    payment.status = PaymentStatus.failed
                
                webhook_log.processed = True
        
        await db.commit()
        return {"status": "success"}
    
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/webhook/stripe")
async def stripe_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    """Handle Stripe webhook"""
    
    payload_bytes = await request.body()
    payload = json.loads(payload_bytes)
    signature = request.headers.get("stripe-signature", "")
    
    webhook_log = PaymentWebhookLog(
        gateway=PaymentGateway.stripe,
        payload=payload,
        signature=signature,
        is_valid=False,
        processed=False
    )
    db.add(webhook_log)
    
    is_valid = StripeGateway.verify_webhook(payload_bytes.decode(), signature)
    webhook_log.is_valid = is_valid
    
    if not is_valid:
        await db.commit()
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    try:
        event_type = payload.get("type")
        
        if event_type == "payment_intent.succeeded":
            payment_intent = payload.get("data", {}).get("object", {})
            booking_id = payment_intent.get("metadata", {}).get("booking_id")
            
            if booking_id:
                result = await db.execute(
                    select(Payment).where(Payment.booking_id == int(booking_id))
                )
                payment = result.scalar_one_or_none()
                
                if payment:
                    payment.status = PaymentStatus.success
                    
                    booking_result = await db.execute(
                        select(Booking).where(Booking.id == payment.booking_id)
                    )
                    booking = booking_result.scalar_one()
                    booking.status = BookingStatus.confirmed
                    
                    background_tasks.add_task(
                        BookingEngine.fire_webhook,
                        {"booking_id": booking.id, "status": "confirmed"}
                    )
                    
                    webhook_log.processed = True
        
        elif event_type == "payment_intent.payment_failed":
            payment_intent = payload.get("data", {}).get("object", {})
            booking_id = payment_intent.get("metadata", {}).get("booking_id")
            
            if booking_id:
                result = await db.execute(
                    select(Payment).where(Payment.booking_id == int(booking_id))
                )
                payment = result.scalar_one_or_none()
                
                if payment:
                    payment.status = PaymentStatus.failed
                    webhook_log.processed = True
        
        await db.commit()
        return {"status": "success"}
    
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/bookings/{booking_id}/cancel")
async def cancel_booking(
    booking_id: int,
    current_user: User = Depends(require_role(UserRole.admin, UserRole.superadmin)),
    db: AsyncSession = Depends(get_db)
):
    """Cancel booking and refund payment (admin only)"""
    
    result = await db.execute(
        select(Booking).where(Booking.id == booking_id)
    )
    booking = result.scalar_one_or_none()
    
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    payment_result = await db.execute(
        select(Payment).where(Payment.booking_id == booking_id)
    )
    payment = payment_result.scalar_one_or_none()
    
    if payment and payment.status == PaymentStatus.success:
        refund_success = False
        
        if payment.gateway == PaymentGateway.paymob:
            refund_success = await PaymobGateway.refund_payment(
                payment.gateway_payment_id,
                payment.amount
            )
        elif payment.gateway == PaymentGateway.stripe:
            refund_success = await StripeGateway.refund_payment(
                payment.gateway_payment_id,
                payment.amount
            )
        
        if refund_success:
            payment.status = PaymentStatus.refunded
    
    booking.status = BookingStatus.cancelled
    
    await db.commit()
    
    return {
        "booking_id": booking_id,
        "status": "cancelled",
        "refund_initiated": payment.status == PaymentStatus.refunded if payment else False
    }

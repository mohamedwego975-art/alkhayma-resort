"""Notification API endpoints for email and WhatsApp."""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional, List

from app.services.email import EmailService, get_email_service
from app.services.whatsapp import WhatsAppService, get_whatsapp_service

router = APIRouter(prefix="/notifications", tags=["notifications"])


class EmailRequest(BaseModel):
    """Request to send an email."""
    to_email: EmailStr
    subject: str
    html_content: str
    text_content: Optional[str] = None


class WhatsAppRequest(BaseModel):
    """Request to send a WhatsApp message."""
    to_number: str
    message: str


class BookingConfirmationRequest(BaseModel):
    """Request to send booking confirmation."""
    to_email: Optional[EmailStr] = None
    to_whatsapp: Optional[str] = None
    guest_name: str
    booking_id: str
    room_name: str
    check_in: str
    check_out: str
    total_amount: float


class CheckInReminderRequest(BaseModel):
    """Request to send check-in reminder."""
    to_email: Optional[EmailStr] = None
    to_whatsapp: Optional[str] = None
    guest_name: str
    booking_id: str
    check_in_date: str
    check_in_time: str = "3:00 PM"


@router.post("/email/send")
async def send_email(
    request: EmailRequest,
    email_service: EmailService = Depends(get_email_service)
):
    """Send a custom email."""
    success = await email_service.send_email(
        to_email=request.to_email,
        subject=request.subject,
        html_content=request.html_content,
        text_content=request.text_content
    )
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to send email")
    
    return {"status": "success", "message": "Email sent successfully"}


@router.post("/whatsapp/send")
async def send_whatsapp(
    request: WhatsAppRequest,
    whatsapp_service: WhatsAppService = Depends(get_whatsapp_service)
):
    """Send a WhatsApp message."""
    success = await whatsapp_service.send_message(
        to_number=request.to_number,
        message=request.message
    )
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to send WhatsApp message")
    
    return {"status": "success", "message": "WhatsApp message sent successfully"}


@router.post("/booking/confirmation")
async def send_booking_confirmation(
    request: BookingConfirmationRequest,
    email_service: EmailService = Depends(get_email_service),
    whatsapp_service: WhatsAppService = Depends(get_whatsapp_service)
):
    """Send booking confirmation via email and/or WhatsApp."""
    results = {}
    
    if request.to_email:
        email_success = await email_service.send_booking_confirmation(
            to_email=request.to_email,
            guest_name=request.guest_name,
            booking_id=request.booking_id,
            room_name=request.room_name,
            check_in=request.check_in,
            check_out=request.check_out,
            total_amount=request.total_amount
        )
        results["email"] = "sent" if email_success else "failed"
    
    if request.to_whatsapp:
        whatsapp_success = await whatsapp_service.send_booking_confirmation(
            to_number=request.to_whatsapp,
            guest_name=request.guest_name,
            booking_id=request.booking_id,
            room_name=request.room_name,
            check_in=request.check_in,
            check_out=request.check_out,
            total_amount=request.total_amount
        )
        results["whatsapp"] = "sent" if whatsapp_success else "failed"
    
    if not results:
        raise HTTPException(status_code=400, detail="No notification method specified")
    
    return {"status": "success", "results": results}


@router.post("/booking/check-in-reminder")
async def send_check_in_reminder(
    request: CheckInReminderRequest,
    email_service: EmailService = Depends(get_email_service),
    whatsapp_service: WhatsAppService = Depends(get_whatsapp_service)
):
    """Send check-in reminder via email and/or WhatsApp."""
    results = {}
    
    if request.to_email:
        email_success = await email_service.send_check_in_reminder(
            to_email=request.to_email,
            guest_name=request.guest_name,
            booking_id=request.booking_id,
            check_in_date=request.check_in_date,
            check_in_time=request.check_in_time
        )
        results["email"] = "sent" if email_success else "failed"
    
    if request.to_whatsapp:
        whatsapp_success = await whatsapp_service.send_check_in_reminder(
            to_number=request.to_whatsapp,
            guest_name=request.guest_name,
            booking_id=request.booking_id,
            check_in_date=request.check_in_date,
            check_in_time=request.check_in_time
        )
        results["whatsapp"] = "sent" if whatsapp_success else "failed"
    
    if not results:
        raise HTTPException(status_code=400, detail="No notification method specified")
    
    return {"status": "success", "results": results}


@router.get("/status")
async def get_notification_status(
    email_service: EmailService = Depends(get_email_service),
    whatsapp_service: WhatsAppService = Depends(get_whatsapp_service)
):
    """Get status of notification services."""
    return {
        "email": {
            "configured": email_service._initialized if hasattr(email_service, '_initialized') else False,
            "from_email": email_service.settings.smtp_from_email if hasattr(email_service, 'settings') else None
        },
        "whatsapp": {
            "configured": whatsapp_service._initialized if hasattr(whatsapp_service, '_initialized') else False,
            "from_number": whatsapp_service.settings.whatsapp_from if hasattr(whatsapp_service, 'settings') else None
        }
    }

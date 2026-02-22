"""WhatsApp notification service using Twilio."""

from typing import Optional
import structlog
from pydantic_settings import BaseSettings

logger = structlog.get_logger()


class WhatsAppSettings(BaseSettings):
    """WhatsApp settings from environment variables."""
    account_sid: str = ""
    auth_token: str = ""
    whatsapp_from: str = "whatsapp:+14155238886"  # Twilio sandbox number
    enabled: bool = False
    
    class Config:
        env_prefix = "TWILIO_"
        case_sensitive = False


class WhatsAppService:
    """Service for sending WhatsApp messages via Twilio."""
    
    def __init__(self, settings: Optional[WhatsAppSettings] = None):
        self.settings = settings or WhatsAppSettings()
        self._client = None
        self._initialized = False
        
    async def initialize(self):
        """Initialize the WhatsApp service."""
        if not self.settings.account_sid or not self.settings.auth_token:
            logger.warning("WhatsApp service not configured - Twilio credentials missing")
            return
        
        try:
            from twilio.rest import Client
            self._client = Client(self.settings.account_sid, self.settings.auth_token)
            self._initialized = True
            logger.info("WhatsApp service initialized")
        except Exception as e:
            logger.error("Failed to initialize WhatsApp service", error=str(e))
    
    def _format_number(self, phone_number: str) -> str:
        """Format phone number to WhatsApp format."""
        # Remove spaces and ensure starts with whatsapp:
        clean_number = phone_number.replace(" ", "").replace("-", "")
        if not clean_number.startswith("whatsapp:"):
            # Ensure number starts with +
            if not clean_number.startswith("+"):
                clean_number = "+" + clean_number
            clean_number = f"whatsapp:{clean_number}"
        return clean_number
    
    async def send_message(
        self,
        to_number: str,
        message: str,
        media_url: Optional[str] = None
    ) -> bool:
        """Send a WhatsApp message."""
        if not self._initialized:
            logger.error("WhatsApp service not initialized")
            return False
        
        try:
            from_number = self._format_number(self.settings.whatsapp_from)
            to_formatted = self._format_number(to_number)
            
            # Create message parameters
            message_params = {
                "body": message,
                "from_": from_number,
                "to": to_formatted
            }
            
            if media_url:
                message_params["media_url"] = [media_url]
            
            # Send message
            msg = self._client.messages.create(**message_params)
            
            logger.info(
                "WhatsApp message sent",
                to=to_number,
                message_sid=msg.sid,
                status=msg.status
            )
            return True
            
        except Exception as e:
            logger.error("Failed to send WhatsApp message", error=str(e), to=to_number)
            return False
    
    async def send_booking_confirmation(
        self,
        to_number: str,
        guest_name: str,
        booking_id: str,
        room_name: str,
        check_in: str,
        check_out: str,
        total_amount: float
    ) -> bool:
        """Send booking confirmation via WhatsApp."""
        message = f"""🏖️ *AlKhayma Beach Resort - Booking Confirmed!*

Dear {guest_name},

Your booking has been confirmed. Here are your details:

📋 *Booking ID:* {booking_id}
🛏️ *Room:* {room_name}
📅 *Check-in:* {check_in}
📅 *Check-out:* {check_out}
💰 *Total:* ${total_amount:.2f}

We look forward to welcoming you! 🌴

Questions? Reply to this message or call us.

🌊 Where Luxury Meets the Sea 🌊"""
        
        return await self.send_message(to_number, message)
    
    async def send_check_in_reminder(
        self,
        to_number: str,
        guest_name: str,
        booking_id: str,
        check_in_date: str,
        check_in_time: str = "3:00 PM"
    ) -> bool:
        """Send check-in reminder via WhatsApp."""
        message = f"""⏰ *AlKhayma Beach Resort - Check-in Reminder*

Hi {guest_name},

Your stay starts soon!

📅 *Check-in Date:* {check_in_date}
🕐 *Check-in Time:* {check_in_time}
📋 *Booking ID:* {booking_id}

Don't forget:
✅ Valid ID/Passport
✅ Booking confirmation
✅ Credit card

Need early check-in? Contact us!

Can't wait to see you! 🌴"""
        
        return await self.send_message(to_number, message)
    
    async def send_check_out_reminder(
        self,
        to_number: str,
        guest_name: str,
        booking_id: str,
        check_out_date: str,
        check_out_time: str = "12:00 PM"
    ) -> bool:
        """Send check-out reminder via WhatsApp."""
        message = f"""👋 *AlKhayma Beach Resort - Check-out Reminder*

Hi {guest_name},

Just a friendly reminder:

📅 *Check-out Date:* {check_out_date}
🕐 *Check-out Time:* {check_out_time}
📋 *Booking ID:* {booking_id}

Need late check-out? Ask at reception or contact us!

Thank you for staying with us! 🌴
We'd love to see you again soon."""
        
        return await self.send_message(to_number, message)
    
    async def send_payment_confirmation(
        self,
        to_number: str,
        guest_name: str,
        amount: float,
        payment_id: str,
        payment_method: str
    ) -> bool:
        """Send payment confirmation via WhatsApp."""
        message = f"""💳 *AlKhayma Beach Resort - Payment Received*

Hi {guest_name},

We received your payment:

💰 *Amount:* ${amount:.2f}
📋 *Payment ID:* {payment_id}
💳 *Method:* {payment_method}

✅ Payment confirmed!

Thank you! 🌴"""
        
        return await self.send_message(to_number, message)
    
    async def send_promotional_message(
        self,
        to_number: str,
        message: str,
        image_url: Optional[str] = None
    ) -> bool:
        """Send promotional message via WhatsApp."""
        formatted_message = f"""🏖️ *AlKhayma Beach Resort*

{message}

Book now: https://alkhayma-resort.com
📞 Contact: info@alkhayma-resort.com

🌊 Where Luxury Meets the Sea 🌊"""
        
        return await self.send_message(to_number, formatted_message, image_url)
    
    async def send_template_message(
        self,
        to_number: str,
        template_name: str,
        language_code: str = "en",
        components: Optional[list] = None
    ) -> bool:
        """Send a template message (requires Twilio approved templates)."""
        if not self._initialized:
            logger.error("WhatsApp service not initialized")
            return False
        
        try:
            from_number = self._format_number(self.settings.whatsapp_from)
            to_formatted = self._format_number(to_number)
            
            # For template messages, use content SID
            msg = self._client.messages.create(
                from_=from_number,
                content_sid=template_name,
                content_variables=components or {},
                to=to_formatted
            )
            
            logger.info(
                "WhatsApp template message sent",
                to=to_number,
                template=template_name,
                message_sid=msg.sid
            )
            return True
            
        except Exception as e:
            logger.error("Failed to send template message", error=str(e))
            return False


# Global WhatsApp service instance
whatsapp_service = WhatsAppService()


async def get_whatsapp_service() -> WhatsAppService:
    """Get the WhatsApp service instance."""
    return whatsapp_service

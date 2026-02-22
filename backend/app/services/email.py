"""Email service for sending emails via SMTP/Gmail."""

import asyncio
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, List
import structlog
from pydantic_settings import BaseSettings

logger = structlog.get_logger()


class EmailSettings(BaseSettings):
    """Email settings from environment variables."""
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_from_name: str = "AlKhayma Resort"
    smtp_from_email: str = ""
    smtp_tls: bool = True
    
    class Config:
        env_prefix = "SMTP_"
        case_sensitive = False


class EmailService:
    """Service for sending emails."""
    
    def __init__(self, settings: Optional[EmailSettings] = None):
        self.settings = settings or EmailSettings()
        self._initialized = False
        
    async def initialize(self):
        """Initialize the email service."""
        if not self.settings.smtp_user or not self.settings.smtp_password:
            logger.warning("Email service not configured - SMTP credentials missing")
            return
        
        self._initialized = True
        logger.info("Email service initialized", host=self.settings.smtp_host)
    
    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None
    ) -> bool:
        """Send an email to a recipient."""
        if not self._initialized:
            logger.error("Email service not initialized")
            return False
        
        try:
            from_email = self.settings.smtp_from_email or self.settings.smtp_user
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.settings.smtp_from_name} <{from_email}>"
            msg['To'] = to_email
            
            if cc:
                msg['Cc'] = ', '.join(cc)
            
            # Attach parts
            if text_content:
                msg.attach(MIMEText(text_content, 'plain', 'utf-8'))
            msg.attach(MIMEText(html_content, 'html', 'utf-8'))
            
            # Send email using aiosmtplib
            import aiosmtplib
            
            recipients = [to_email]
            if cc:
                recipients.extend(cc)
            if bcc:
                recipients.extend(bcc)
            
            await aiosmtplib.send(
                msg,
                hostname=self.settings.smtp_host,
                port=self.settings.smtp_port,
                username=self.settings.smtp_user,
                password=self.settings.smtp_password,
                start_tls=self.settings.smtp_tls,
                to=recipients,
                mail_from=from_email
            )
            
            logger.info(
                "Email sent successfully",
                to=to_email,
                subject=subject
            )
            return True
            
        except Exception as e:
            logger.error("Failed to send email", error=str(e), to=to_email)
            return False
    
    async def send_booking_confirmation(
        self,
        to_email: str,
        guest_name: str,
        booking_id: str,
        room_name: str,
        check_in: str,
        check_out: str,
        total_amount: float
    ) -> bool:
        """Send booking confirmation email."""
        subject = f"Booking Confirmation - {booking_id}"
        
        html_content = f"""
        <html dir="rtl" lang="ar">
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .booking-details {{ background: white; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                .detail-row {{ display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #eee; }}
                .detail-row:last-child {{ border-bottom: none; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🏖️ الخيمة Beach Resort</h1>
                    <p>Your Luxury Beach Getaway</p>
                </div>
                <div class="content">
                    <h2>Dear {guest_name},</h2>
                    <p>Thank you for choosing AlKhayma Beach Resort! Your booking has been confirmed.</p>
                    
                    <div class="booking-details">
                        <h3>Booking Details</h3>
                        <div class="detail-row">
                            <strong>Booking ID:</strong>
                            <span>{booking_id}</span>
                        </div>
                        <div class="detail-row">
                            <strong>Room:</strong>
                            <span>{room_name}</span>
                        </div>
                        <div class="detail-row">
                            <strong>Check-in:</strong>
                            <span>{check_in}</span>
                        </div>
                        <div class="detail-row">
                            <strong>Check-out:</strong>
                            <span>{check_out}</span>
                        </div>
                        <div class="detail-row">
                            <strong>Total Amount:</strong>
                            <span>${total_amount:.2f}</span>
                        </div>
                    </div>
                    
                    <p>We look forward to welcoming you! If you have any questions, please don't hesitate to contact us.</p>
                    
                    <div class="footer">
                        <p>📧 info@alkhayma-resort.com | 📱 +20 XXX XXX XXXX</p>
                        <p>AlKhayma Beach Resort - Where Luxury Meets the Sea</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        AlKhayma Beach Resort - Booking Confirmation
        
        Dear {guest_name},
        
        Thank you for choosing AlKhayma Beach Resort! Your booking has been confirmed.
        
        Booking Details:
        - Booking ID: {booking_id}
        - Room: {room_name}
        - Check-in: {check_in}
        - Check-out: {check_out}
        - Total Amount: ${total_amount:.2f}
        
        We look forward to welcoming you!
        
        Contact: info@alkhayma-resort.com
        """
        
        return await self.send_email(to_email, subject, html_content, text_content)
    
    async def send_check_in_reminder(
        self,
        to_email: str,
        guest_name: str,
        booking_id: str,
        check_in_date: str,
        check_in_time: str = "3:00 PM"
    ) -> bool:
        """Send check-in reminder email."""
        subject = f"Check-in Reminder - {booking_id}"
        
        html_content = f"""
        <html dir="rtl" lang="ar">
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .reminder-box {{ background: #fff3cd; border: 1px solid #ffc107; padding: 20px; margin: 20px 0; border-radius: 8px; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🏖️ الخيمة Beach Resort</h1>
                    <p>Check-in Reminder</p>
                </div>
                <div class="content">
                    <h2>Dear {guest_name},</h2>
                    <p>Your stay with us is just around the corner!</p>
                    
                    <div class="reminder-box">
                        <h3>⏰ Check-in Details</h3>
                        <p><strong>Date:</strong> {check_in_date}</p>
                        <p><strong>Time:</strong> {check_in_time}</p>
                        <p><strong>Booking ID:</strong> {booking_id}</p>
                    </div>
                    
                    <p>Don't forget to bring:</p>
                    <ul>
                        <li>Valid ID or Passport</li>
                        <li>Booking confirmation</li>
                        <li>Credit card for incidentals</li>
                    </ul>
                    
                    <p>Need early check-in? Contact us at info@alkhayma-resort.com</p>
                    
                    <div class="footer">
                        <p>We can't wait to welcome you! 🌴</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        return await self.send_email(to_email, subject, html_content)
    
    async def send_post_stay_review_request(
        self,
        to_email: str,
        guest_name: str,
        review_link: str
    ) -> bool:
        """Send post-stay review request email."""
        subject = "How was your stay? Share your experience!"
        
        html_content = f"""
        <html dir="rtl" lang="ar">
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .cta-button {{ display: inline-block; background: #667eea; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🏖️ الخيمة Beach Resort</h1>
                    <p>Thank you for staying with us!</p>
                </div>
                <div class="content">
                    <h2>Dear {guest_name},</h2>
                    <p>We hope you had a wonderful time at AlKhayma Beach Resort!</p>
                    <p>Your feedback helps us improve and helps other travelers discover us.</p>
                    
                    <div style="text-align: center;">
                        <a href="{review_link}" class="cta-button">Leave a Review ⭐</a>
                    </div>
                    
                    <p>Thank you for choosing AlKhayma Beach Resort. We hope to see you again soon!</p>
                    
                    <div class="footer">
                        <p>🏖️ Where Luxury Meets the Sea</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        return await self.send_email(to_email, subject, html_content)


# Global email service instance
email_service = EmailService()


async def get_email_service() -> EmailService:
    """Get the email service instance."""
    return email_service

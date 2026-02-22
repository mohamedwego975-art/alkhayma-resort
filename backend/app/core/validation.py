"""
Input validation and sanitization utilities
Provides validators for common input types and sanitization functions
"""

import re
import html
from typing import Optional, List
from datetime import datetime, date
from pydantic import BaseModel, Field, validator, EmailStr
import bleach

# Allowed HTML tags for rich text (if needed)
ALLOWED_TAGS = ['p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li']
ALLOWED_ATTRIBUTES = {}


class ValidationError(Exception):
    """Custom validation error"""
    pass


def sanitize_html(text: Optional[str]) -> Optional[str]:
    """
    Sanitize HTML content to prevent XSS attacks
    
    Args:
        text: Input text that may contain HTML
        
    Returns:
        Sanitized text with only allowed HTML tags
    """
    if not text:
        return text
    
    # First escape HTML entities
    text = html.escape(text)
    
    # Then allow specific safe HTML tags
    return bleach.clean(text, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, strip=True)


def sanitize_string(text: Optional[str], max_length: int = 255) -> Optional[str]:
    """
    Sanitize plain string input
    
    Args:
        text: Input string
        max_length: Maximum allowed length
        
    Returns:
        Sanitized string
    """
    if not text:
        return text
    
    # Remove control characters
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    
    # Trim whitespace
    text = text.strip()
    
    # Limit length
    if len(text) > max_length:
        text = text[:max_length]
    
    return text


def validate_email(email: str) -> bool:
    """
    Validate email address format
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone: str, country_code: Optional[str] = None) -> bool:
    """
    Validate phone number format
    
    Args:
        phone: Phone number to validate
        country_code: Optional country code (e.g., '+20', '+1')
        
    Returns:
        True if valid, False otherwise
    """
    # Remove all non-digit characters except +
    cleaned = re.sub(r'[^\d+]', '', phone)
    
    # Basic validation - should be between 10-15 digits
    digits_only = re.sub(r'\D', '', cleaned)
    
    if len(digits_only) < 10 or len(digits_only) > 15:
        return False
    
    return True


def validate_date_range(check_in: date, check_out: date, max_days: int = 30) -> bool:
    """
    Validate booking date range
    
    Args:
        check_in: Check-in date
        check_out: Check-out date
        max_days: Maximum stay duration
        
    Returns:
        True if valid, False otherwise
    """
    # Check-out must be after check-in
    if check_out <= check_in:
        return False
    
    # Calculate duration
    duration = (check_out - check_in).days
    
    # Check duration limits
    if duration < 1:
        return False
    
    if duration > max_days:
        return False
    
    # Check-in cannot be in the past
    if check_in < date.today():
        return False
    
    return True


def validate_guest_count(guests: int, max_guests: int = 10) -> bool:
    """
    Validate guest count
    
    Args:
        guests: Number of guests
        max_guests: Maximum allowed guests
        
    Returns:
        True if valid, False otherwise
    """
    return 1 <= guests <= max_guests


def validate_price(amount: float, min_price: float = 0, max_price: float = 10000) -> bool:
    """
    Validate price amount
    
    Args:
        amount: Price amount
        min_price: Minimum allowed price
        max_price: Maximum allowed price
        
    Returns:
        True if valid, False otherwise
    """
    return min_price <= amount <= max_price


# Pydantic models for API validation
class BookingCreateValidator(BaseModel):
    """Validation model for booking creation"""
    room_id: int = Field(..., gt=0, description="Room ID must be positive")
    check_in: date
    check_out: date
    guests: int = Field(..., ge=1, le=10, description="Guest count must be between 1 and 10")
    guest_name: str = Field(..., min_length=2, max_length=100)
    guest_email: EmailStr
    guest_phone: str = Field(..., min_length=10, max_length=20)
    special_requests: Optional[str] = Field(None, max_length=500)
    
    @validator('guest_phone')
    def validate_phone_number(cls, v):
        if not validate_phone(v):
            raise ValueError('Invalid phone number format')
        return sanitize_string(v)
    
    @validator('guest_name')
    def validate_name(cls, v):
        sanitized = sanitize_string(v, max_length=100)
        if len(sanitized) < 2:
            raise ValueError('Name must be at least 2 characters')
        return sanitized
    
    @validator('special_requests')
    def validate_requests(cls, v):
        if v:
            return sanitize_html(v)
        return v
    
    @validator('check_out')
    def validate_dates(cls, v, values):
        if 'check_in' in values:
            if not validate_date_range(values['check_in'], v):
                raise ValueError('Invalid date range')
        return v


class ContactFormValidator(BaseModel):
    """Validation model for contact form"""
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    subject: str = Field(..., min_length=3, max_length=100)
    message: str = Field(..., min_length=10, max_length=2000)
    
    @validator('name', 'subject')
    def sanitize_text(cls, v):
        return sanitize_string(v)
    
    @validator('message')
    def sanitize_message(cls, v):
        # Sanitize but preserve line breaks
        sanitized = sanitize_html(v)
        return sanitized
    
    @validator('phone')
    def validate_phone_optional(cls, v):
        if v and not validate_phone(v):
            raise ValueError('Invalid phone number format')
        return sanitize_string(v) if v else v


class ReviewValidator(BaseModel):
    """Validation model for reviews"""
    product_id: int = Field(..., gt=0)
    rating: int = Field(..., ge=1, le=5)
    comment: str = Field(..., min_length=10, max_length=1000)
    user_name: str = Field(..., min_length=2, max_length=50)
    
    @validator('comment')
    def sanitize_comment(cls, v):
        return sanitize_html(v)
    
    @validator('user_name')
    def sanitize_username(cls, v):
        return sanitize_string(v, max_length=50)


def validate_password_strength(password: str) -> tuple[bool, List[str]]:
    """
    Validate password strength
    
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")
    
    if not re.search(r'[A-Z]', password):
        errors.append("Password must contain at least one uppercase letter")
    
    if not re.search(r'[a-z]', password):
        errors.append("Password must contain at least one lowercase letter")
    
    if not re.search(r'\d', password):
        errors.append("Password must contain at least one digit")
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append("Password must contain at least one special character")
    
    return len(errors) == 0, errors

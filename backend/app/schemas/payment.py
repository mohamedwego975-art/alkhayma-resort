from pydantic import BaseModel, Field
from typing import Optional


class InitiatePaymentRequest(BaseModel):
    gateway: str = Field(..., pattern="^(paymob|stripe)$")
    currency: str = Field(..., pattern="^(EGP|USD)$")


class PaymobPaymentResponse(BaseModel):
    payment_url: str
    payment_key: str
    order_id: str


class StripePaymentResponse(BaseModel):
    client_secret: str
    payment_intent_id: str


class PaymentResponse(BaseModel):
    payment_id: int
    gateway: str
    amount: str
    currency: str
    paymob_data: Optional[PaymobPaymentResponse] = None
    stripe_data: Optional[StripePaymentResponse] = None

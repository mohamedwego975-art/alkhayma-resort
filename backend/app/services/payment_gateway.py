import httpx
import hashlib
import hmac
from decimal import Decimal
from typing import Dict, Any
from fastapi import HTTPException
from app.core.config import settings


class PaymentGateway:
    """Base payment gateway interface"""
    
    @staticmethod
    async def initiate_payment(amount: Decimal, currency: str, booking_id: int, user_data: Dict) -> Dict[str, Any]:
        raise NotImplementedError
    
    @staticmethod
    def verify_webhook(payload: Dict, signature: str) -> bool:
        raise NotImplementedError
    
    @staticmethod
    async def refund_payment(gateway_payment_id: str, amount: Decimal) -> bool:
        raise NotImplementedError


class PaymobGateway(PaymentGateway):
    """Paymob payment gateway (Egyptian market)"""
    
    BASE_URL = "https://accept.paymob.com/api"
    
    @staticmethod
    async def get_auth_token() -> str:
        """Step 1: Authenticate with Paymob"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{PaymobGateway.BASE_URL}/auth/tokens",
                    json={"api_key": settings.paymob_api_key},
                    timeout=10.0
                )
                response.raise_for_status()
                return response.json()["token"]
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Paymob authentication failed: {str(e)}")
    
    @staticmethod
    async def create_order(auth_token: str, amount: Decimal, booking_id: int) -> str:
        """Step 2: Create order"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{PaymobGateway.BASE_URL}/ecommerce/orders",
                    json={
                        "auth_token": auth_token,
                        "delivery_needed": "false",
                        "amount_cents": int(amount * 100),
                        "currency": "EGP",
                        "merchant_order_id": booking_id,
                        "items": []
                    },
                    timeout=10.0
                )
                response.raise_for_status()
                return str(response.json()["id"])
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Paymob order creation failed: {str(e)}")
    
    @staticmethod
    async def get_payment_key(auth_token: str, order_id: str, amount: Decimal, user_data: Dict) -> str:
        """Step 3: Register payment key"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{PaymobGateway.BASE_URL}/acceptance/payment_keys",
                json={
                    "auth_token": auth_token,
                    "amount_cents": int(amount * 100),
                    "expiration": 3600,
                    "order_id": order_id,
                    "billing_data": {
                        "email": user_data.get("email", "customer@example.com"),
                        "first_name": user_data.get("first_name", "Customer"),
                        "last_name": user_data.get("last_name", "User"),
                        "phone_number": user_data.get("phone", "+201000000000"),
                        "apartment": "NA",
                        "floor": "NA",
                        "street": "NA",
                        "building": "NA",
                        "shipping_method": "NA",
                        "postal_code": "NA",
                        "city": "NA",
                        "country": "EG",
                        "state": "NA"
                    },
                    "currency": "EGP",
                    "integration_id": settings.paymob_integration_id
                }
            )
            return response.json()["token"]
    
    @staticmethod
    async def initiate_payment(amount: Decimal, currency: str, booking_id: int, user_data: Dict) -> Dict[str, Any]:
        """Complete Paymob payment flow"""
        auth_token = await PaymobGateway.get_auth_token()
        order_id = await PaymobGateway.create_order(auth_token, amount, booking_id)
        payment_key = await PaymobGateway.get_payment_key(auth_token, order_id, amount, user_data)
        payment_url = f"https://accept.paymob.com/api/acceptance/iframes/{settings.paymob_integration_id}?payment_token={payment_key}"
        
        return {
            "payment_url": payment_url,
            "payment_key": payment_key,
            "order_id": order_id
        }
    
    @staticmethod
    def verify_webhook(payload: Dict, signature: str) -> bool:
        """Verify Paymob HMAC signature"""
        concat_string = (
            f"{payload.get('amount_cents', '')}"
            f"{payload.get('created_at', '')}"
            f"{payload.get('currency', '')}"
            f"{payload.get('error_occured', '')}"
            f"{payload.get('has_parent_transaction', '')}"
            f"{payload.get('id', '')}"
            f"{payload.get('integration_id', '')}"
            f"{payload.get('is_3d_secure', '')}"
            f"{payload.get('is_auth', '')}"
            f"{payload.get('is_capture', '')}"
            f"{payload.get('is_refunded', '')}"
            f"{payload.get('is_standalone_payment', '')}"
            f"{payload.get('is_voided', '')}"
            f"{payload.get('order', {}).get('id', '')}"
            f"{payload.get('owner', '')}"
            f"{payload.get('pending', '')}"
            f"{payload.get('source_data', {}).get('pan', '')}"
            f"{payload.get('source_data', {}).get('sub_type', '')}"
            f"{payload.get('source_data', {}).get('type', '')}"
            f"{payload.get('success', '')}"
        )
        
        calculated_hmac = hmac.new(
            settings.paymob_hmac_secret.encode(),
            concat_string.encode(),
            hashlib.sha512
        ).hexdigest()
        
        return hmac.compare_digest(calculated_hmac, signature)
    
    @staticmethod
    async def refund_payment(gateway_payment_id: str, amount: Decimal) -> bool:
        """Initiate Paymob refund"""
        auth_token = await PaymobGateway.get_auth_token()
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{PaymobGateway.BASE_URL}/acceptance/void_refund/refund",
                json={
                    "auth_token": auth_token,
                    "transaction_id": gateway_payment_id,
                    "amount_cents": int(amount * 100)
                }
            )
            return response.status_code == 200


class StripeGateway(PaymentGateway):
    """Stripe payment gateway (international)"""
    
    @staticmethod
    async def initiate_payment(amount: Decimal, currency: str, booking_id: int, user_data: Dict) -> Dict[str, Any]:
        """Create Stripe PaymentIntent"""
        try:
            import stripe
            stripe.api_key = settings.stripe_secret_key
            
            intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),
                currency=currency.lower(),
                metadata={"booking_id": booking_id},
                automatic_payment_methods={"enabled": True}
            )
            
            return {
                "client_secret": intent.client_secret,
                "payment_intent_id": intent.id
            }
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Stripe payment initiation failed: {str(e)}")
    
    @staticmethod
    def verify_webhook(payload: str, signature: str) -> bool:
        """Verify Stripe webhook signature"""
        import stripe
        stripe.api_key = settings.stripe_secret_key
        
        try:
            stripe.Webhook.construct_event(
                payload, signature, settings.stripe_webhook_secret
            )
            return True
        except Exception:
            return False
    
    @staticmethod
    async def refund_payment(gateway_payment_id: str, amount: Decimal) -> bool:
        """Initiate Stripe refund"""
        import stripe
        stripe.api_key = settings.stripe_secret_key
        
        try:
            stripe.Refund.create(
                payment_intent=gateway_payment_id,
                amount=int(amount * 100)
            )
            return True
        except Exception:
            return False

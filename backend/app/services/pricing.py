from dataclasses import dataclass, field
from decimal import Decimal
from datetime import date, timedelta
from typing import List, Dict


@dataclass
class PriceBreakdown:
    base_price: Decimal
    final_price: Decimal
    nightly_rate: Decimal
    discounts: List[Dict[str, Decimal]] = field(default_factory=list)
    multipliers: List[Dict[str, Decimal]] = field(default_factory=list)
    total_savings: Decimal = Decimal("0.00")
    currency: str = "USD"


class PricingEngine:
    # Eid holidays (approximate dates for 2026)
    EID_HOLIDAYS = [
        (date(2026, 3, 20), date(2026, 3, 24)),  # Eid al-Fitr
        (date(2026, 6, 6), date(2026, 6, 10)),   # Eid al-Adha
    ]
    
    @staticmethod
    def is_high_season(check_date: date) -> bool:
        """Check if date is in high season (Jul-Aug + Eid holidays)"""
        # July-August
        if check_date.month in [7, 8]:
            return True
        
        # Eid holidays
        for eid_start, eid_end in PricingEngine.EID_HOLIDAYS:
            if eid_start <= check_date <= eid_end:
                return True
        
        return False
    
    @staticmethod
    def is_medium_season(check_date: date) -> bool:
        """Check if date is in medium season (Mar-Jun, Sep-Oct)"""
        return check_date.month in [3, 4, 5, 6, 9, 10]
    
    @staticmethod
    def get_seasonal_multiplier(check_date: date) -> Decimal:
        """Get seasonal multiplier for a date"""
        if PricingEngine.is_high_season(check_date):
            return Decimal("1.40")
        elif PricingEngine.is_medium_season(check_date):
            return Decimal("1.15")
        else:  # Low season (Nov-Feb)
            return Decimal("0.90")
    
    @staticmethod
    def count_weekend_nights(check_in: date, nights: int) -> int:
        """Count Friday nights in the stay"""
        weekend_count = 0
        for i in range(nights):
            current_date = check_in + timedelta(days=i)
            if current_date.weekday() == 4:  # Friday = 4
                weekend_count += 1
        return weekend_count
    
    @staticmethod
    def calculate(
        base_price: Decimal,
        product_type: str,
        check_in: date,
        nights: int,
        days_ahead: int,
        quantity: int = 1
    ) -> PriceBreakdown:
        """
        Calculate price with all rules applied in order:
        1. Seasonal multiplier
        2. Weekend surge
        3. Early booking discount
        4. Long stay discount
        5. Last minute surge (overrides early booking)
        """
        
        base_price = Decimal(str(base_price))
        multipliers = []
        discounts = []
        
        # Start with base price
        current_price = base_price
        
        # 1. SEASONAL MULTIPLIER (apply to base)
        seasonal_multiplier = PricingEngine.get_seasonal_multiplier(check_in)
        if seasonal_multiplier != Decimal("1.00"):
            multipliers.append({
                "reason": f"Seasonal adjustment ({'High' if seasonal_multiplier == Decimal('1.40') else 'Medium' if seasonal_multiplier == Decimal('1.15') else 'Low'} season)",
                "factor": seasonal_multiplier
            })
            current_price *= seasonal_multiplier
        
        # Calculate nightly rate after seasonal adjustment
        nightly_rate = current_price
        
        # 2. WEEKEND SURGE (+15% per weekend night)
        weekend_nights = PricingEngine.count_weekend_nights(check_in, nights)
        if weekend_nights > 0:
            weekend_premium = nightly_rate * Decimal("0.15") * weekend_nights
            multipliers.append({
                "reason": f"Weekend premium ({weekend_nights} night{'s' if weekend_nights > 1 else ''})",
                "factor": Decimal("1.15")
            })
            current_price = (nightly_rate * nights) + weekend_premium
        else:
            current_price = nightly_rate * nights
        
        # 3. EARLY BOOKING DISCOUNT
        early_discount = Decimal("0.00")
        if days_ahead >= 60:
            early_discount = Decimal("0.20")
            discounts.append({
                "reason": "Early booking (60+ days)",
                "amount": current_price * early_discount
            })
        elif days_ahead >= 30:
            early_discount = Decimal("0.15")
            discounts.append({
                "reason": "Early booking (30+ days)",
                "amount": current_price * early_discount
            })
        
        if early_discount > 0:
            current_price *= (Decimal("1.00") - early_discount)
        
        # 4. LONG STAY DISCOUNT
        long_stay_discount = Decimal("0.00")
        if nights >= 10:
            long_stay_discount = Decimal("0.18")
            discounts.append({
                "reason": "Long stay (10+ nights)",
                "amount": current_price * long_stay_discount
            })
        elif nights >= 5:
            long_stay_discount = Decimal("0.10")
            discounts.append({
                "reason": "Long stay (5+ nights)",
                "amount": current_price * long_stay_discount
            })
        
        if long_stay_discount > 0:
            current_price *= (Decimal("1.00") - long_stay_discount)
        
        # 5. LAST MINUTE SURGE (overrides early booking)
        if days_ahead <= 2:
            # Remove early booking discount if applied
            if early_discount > 0:
                # Reverse early booking discount
                current_price /= (Decimal("1.00") - early_discount)
                discounts = [d for d in discounts if "Early booking" not in d["reason"]]
            
            # Apply last minute surge
            last_minute_surge = current_price * Decimal("0.25")
            multipliers.append({
                "reason": "Last minute booking",
                "factor": Decimal("1.25")
            })
            current_price *= Decimal("1.25")
        
        # Apply quantity
        final_price = current_price * quantity
        
        # Calculate total savings
        total_base = base_price * nights * quantity
        total_savings = total_base - final_price if final_price < total_base else Decimal("0.00")
        
        # Round to 2 decimal places
        final_price = final_price.quantize(Decimal("0.01"))
        nightly_rate = nightly_rate.quantize(Decimal("0.01"))
        total_savings = total_savings.quantize(Decimal("0.01"))
        
        return PriceBreakdown(
            base_price=base_price,
            final_price=final_price,
            nightly_rate=nightly_rate,
            discounts=discounts,
            multipliers=multipliers,
            total_savings=total_savings,
            currency="USD"
        )

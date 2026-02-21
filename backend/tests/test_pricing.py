import pytest
from decimal import Decimal
from datetime import date, timedelta
from app.services.pricing import PricingEngine


def test_early_booking_discount():
    """Test early booking discount: 35 days ahead → expect -15%"""
    base_price = Decimal("100.00")
    # Use a date in low season (February) to avoid seasonal multiplier
    check_in = date(2026, 2, 15)
    nights = 3
    days_ahead = 35
    
    result = PricingEngine.calculate(
        base_price=base_price,
        product_type="room",
        check_in=check_in,
        nights=nights,
        days_ahead=days_ahead,
        quantity=1
    )
    
    # Base: 100 * 0.90 (low season) = 90 per night
    # Total: 90 * 3 = 270
    # Early booking -15%: 270 * 0.85 = 229.50
    expected = Decimal("229.50")
    
    # Check if early booking discount is applied
    assert any("Early booking" in d["reason"] for d in result.discounts), "Early booking discount not found"
    assert result.final_price == expected, f"Expected {expected}, got {result.final_price}"
    print(f"✅ Early booking test passed: {result.final_price}")


def test_last_minute_surge():
    """Test last minute surge: 1 day ahead → expect +25%"""
    base_price = Decimal("100.00")
    # Use a date in low season (January) - Monday to avoid weekend
    check_in = date(2027, 1, 11)  # Monday
    nights = 2  # Mon-Tue, Tue-Wed (no weekend)
    days_ahead = 1
    
    result = PricingEngine.calculate(
        base_price=base_price,
        product_type="room",
        check_in=check_in,
        nights=nights,
        days_ahead=days_ahead,
        quantity=1
    )
    
    # Base: 100 * 0.90 (low season) = 90 per night
    # Total: 90 * 2 = 180
    # Last minute +25%: 180 * 1.25 = 225
    expected = Decimal("225.00")
    
    # Check if last minute surge is applied
    assert any("Last minute" in m["reason"] for m in result.multipliers), "Last minute surge not found"
    assert result.final_price == expected, f"Expected {expected}, got {result.final_price}"
    print(f"✅ Last minute test passed: {result.final_price}")


def test_long_stay_discount():
    """Test long stay discount: 7 nights → expect -10%"""
    base_price = Decimal("100.00")
    # Use a date in low season (November) - Monday
    check_in = date(2026, 11, 2)  # Monday
    nights = 7  # Mon-Sun (includes Fri+Sat)
    days_ahead = 10
    
    result = PricingEngine.calculate(
        base_price=base_price,
        product_type="room",
        check_in=check_in,
        nights=nights,
        days_ahead=days_ahead,
        quantity=1
    )
    
    # Base: 100 * 0.90 (low season) = 90 per night
    # Weekend premium: 90 * 0.15 * 1 (only Friday, not Saturday) = 13.50
    # Total: (90 * 7) + 13.50 = 643.50
    # Long stay -10%: 643.50 * 0.90 = 579.15
    expected = Decimal("579.15")
    
    # Check if long stay discount is applied
    assert any("Long stay" in d["reason"] for d in result.discounts), "Long stay discount not found"
    assert result.final_price == expected, f"Expected {expected}, got {result.final_price}"
    print(f"✅ Long stay test passed: {result.final_price}")


def test_weekend_within_stay():
    """Test weekend premium: stay includes Friday → expect weekend premium"""
    base_price = Decimal("100.00")
    
    # Use specific date: Thursday Jan 15, 2027 (low season, no other modifiers)
    check_in = date(2027, 1, 14)  # Thursday
    nights = 2  # Thu-Fri, Fri-Sat (includes Friday night)
    days_ahead = 10
    
    result = PricingEngine.calculate(
        base_price=base_price,
        product_type="room",
        check_in=check_in,
        nights=nights,
        days_ahead=days_ahead,
        quantity=1
    )
    
    # Base: 100 * 0.90 (low season) = 90 per night
    # Weekend premium: 90 * 0.15 * 1 (Friday) = 13.50
    # Total: (90 * 2) + 13.50 = 193.50
    expected = Decimal("193.50")
    
    # Check if weekend premium is applied
    assert any("Weekend premium" in m["reason"] for m in result.multipliers), "Weekend premium not found"
    assert result.final_price == expected, f"Expected {expected}, got {result.final_price}"
    print(f"✅ Weekend test passed: {result.final_price}")


def test_high_season():
    """Test high season: August date → expect ×1.40"""
    base_price = Decimal("100.00")
    check_in = date(2026, 8, 15)  # August (high season)
    nights = 3
    days_ahead = 10  # Not early booking, not last minute
    
    result = PricingEngine.calculate(
        base_price=base_price,
        product_type="room",
        check_in=check_in,
        nights=nights,
        days_ahead=days_ahead,
        quantity=1
    )
    
    # Base: 100 * 1.40 (high season) = 140 per night
    # Total: 140 * 3 = 420
    expected = Decimal("420.00")
    
    # Check if high season multiplier is applied
    assert any("High season" in m["reason"] for m in result.multipliers), "High season multiplier not found"
    assert result.final_price == expected, f"Expected {expected}, got {result.final_price}"
    print(f"✅ High season test passed: {result.final_price}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])

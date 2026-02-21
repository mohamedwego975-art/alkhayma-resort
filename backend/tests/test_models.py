import pytest
from app.models import Product, ProductType


def test_product_model():
    product = Product(
        name="Deluxe Room",
        name_ar="غرفة ديلوكس",
        slug="deluxe-room",
        type=ProductType.room,
        base_price=500.00,
        capacity=2,
        description="Luxury room with sea view",
        is_active=True,
        sort_order=1
    )
    
    assert product.name == "Deluxe Room"
    assert product.type == ProductType.room
    assert product.base_price == 500.00
    assert product.is_active is True
    assert product.sort_order == 1

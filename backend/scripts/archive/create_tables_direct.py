#!/usr/bin/env python
"""
Create all database tables using SQLAlchemy metadata
"""
import sys
import asyncio
from sqlalchemy import inspect
from app.core.database import engine, Base
from app.models.room import Room
from app.models.user import User
from app.models.product import Product
from app.models.booking import Booking
from app.models.payment import Payment
from app.models.review import Review
from app.models.package import Package, PackageItem
from app.models.blog import BlogPost
from app.models.audit import AuditLog
from app.models.inventory import Inventory
from app.models.loyalty import LoyaltyAccount, LoyaltyTransaction
from app.models.recommendation import Recommendation


def create_all_tables():
    """Create all tables defined in Base"""
    try:
        # Check existing tables
        inspector = inspect(engine.sync_engine)
        existing_tables = inspector.get_table_names()
        print(f"Existing tables: {existing_tables}")

        # Create all tables
        Base.metadata.create_all(bind=engine.sync_engine)
        print("✅ All tables created successfully!")

        # Verify
        inspector = inspect(engine.sync_engine)
        new_tables = inspector.get_table_names()
        print(f"New tables: {new_tables}")

        if "rooms" in new_tables:
            columns = [col["name"] for col in inspector.get_columns("rooms")]
            print(f"✅ Rooms table columns: {columns}")

    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    create_all_tables()

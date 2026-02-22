#!/usr/bin/env python3
"""Quick seed script for development"""
import asyncio
import sys
sys.path.insert(0, '/home/wego/Desktop/alkhayma-resort/backend')

from app.core.database import AsyncSessionLocal, engine, Base
from app.models import Room, Product, User
from app.core.security import get_password_hash
from sqlalchemy import select, func

async def main():
    print("Creating tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncSessionLocal() as session:
        # Rooms
        r = await session.scalar(select(func.count()).select_from(Room))
        if r == 0:
            rooms = [
                Room(room_number='101', room_type='deluxe', price_per_night=150.0, capacity=2, is_active=True, description_en='Luxury sea view room', rating=4.5),
                Room(room_number='102', room_type='deluxe', price_per_night=150.0, capacity=2, is_active=True, description_en='Luxury sea view room', rating=4.3),
                Room(room_number='201', room_type='suite', price_per_night=250.0, capacity=4, is_active=True, description_en='Premium suite', rating=4.8),
                Room(room_number='301', room_type='standard', price_per_night=80.0, capacity=2, is_active=True, description_en='Standard room', rating=4.0),
            ]
            for room in rooms:
                session.add(room)
            await session.commit()
            print(f"✅ Added {len(rooms)} rooms")
        else:
            print(f"ℹ️  {r} rooms already exist")
        
        # Products
        p = await session.scalar(select(func.count()).select_from(Product))
        if p == 0:
            products = [
                Product(name='VIP Beach Cabana', base_price=65.0, product_type='beach', is_active=True),
                Product(name='Standard Beach Spot', base_price=25.0, product_type='beach', is_active=True),
                Product(name='Sunset Dinner', base_price=150.0, product_type='activity', is_active=True),
            ]
            for prod in products:
                session.add(prod)
            await session.commit()
            print(f"✅ Added {len(products)} products")
        else:
            print(f"ℹ️  {p} products already exist")
        
        # Users
        u = await session.scalar(select(func.count()).select_from(User))
        if u == 0:
            users = [
                User(email='admin@alkhayma.com', full_name='Admin User', hashed_password=get_password_hash('admin123'), role='admin', is_active=True),
                User(email='test@example.com', full_name='Test User', hashed_password=get_password_hash('test123'), role='guest', is_active=True),
            ]
            for user in users:
                session.add(user)
            await session.commit()
            print(f"✅ Added {len(users)} users")
        else:
            print(f"ℹ️  {u} users already exist")
        
        # Final count
        r = await session.scalar(select(func.count()).select_from(Room))
        p = await session.scalar(select(func.count()).select_from(Product))
        u = await session.scalar(select(func.count()).select_from(User))
        print(f"\n✅ DATABASE READY: {r} Rooms, {p} Products, {u} Users")

if __name__ == "__main__":
    asyncio.run(main())

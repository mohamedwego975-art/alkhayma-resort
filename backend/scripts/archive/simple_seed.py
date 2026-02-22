#!/usr/bin/env python3
"""Simple seed script with output"""
import asyncio
import sys
sys.path.insert(0, '/home/wego/Desktop/alkhayma-resort/backend')

from app.core.database import AsyncSessionLocal, engine, Base
from app.models import Room, Product
from sqlalchemy import select, func

async def main():
    print("Creating tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created")
    
    async with AsyncSessionLocal() as session:
        # Rooms
        r = await session.scalar(select(func.count()).select_from(Room))
        if r == 0:
            session.add(Room(room_number='101', room_type='deluxe', price_per_night=150.0, capacity=2, is_active=True, description_en='Luxury room'))
            session.add(Room(room_number='201', room_type='suite', price_per_night=250.0, capacity=4, is_active=True, description_en='Suite'))
            await session.commit()
            print("✅ 2 rooms added")
        else:
            print(f"ℹ️  {r} rooms already exist")
        
        # Products
        p = await session.scalar(select(func.count()).select_from(Product))
        if p == 0:
            session.add(Product(name='VIP Cabana', base_price=65.0, product_type='beach', is_active=True))
            session.add(Product(name='Dinner', base_price=150.0, product_type='activity', is_active=True))
            await session.commit()
            print("✅ 2 products added")
        else:
            print(f"ℹ️  {p} products already exist")
        
        # Count
        r = await session.scalar(select(func.count()).select_from(Room))
        p = await session.scalar(select(func.count()).select_from(Product))
        print(f"✅ Database: {r} rooms, {p} products")

if __name__ == "__main__":
    asyncio.run(main())

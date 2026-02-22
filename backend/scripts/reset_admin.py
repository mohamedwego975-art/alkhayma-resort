"""
Reset admin user password (admin@alkhayma.com).
Run from backend directory: python scripts/reset_admin.py
Set ADMIN_NEW_PASSWORD env var for the new password (default: admin123).
"""
import asyncio
import os
import sys

# Ensure backend root is on path when run as script
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import settings
from app.core.security import get_password_hash


async def main() -> None:
    new_password = os.environ.get("ADMIN_NEW_PASSWORD", "admin123")
    engine = create_async_engine(settings.database_url)
    pass_hash = get_password_hash(new_password)

    async with engine.begin() as conn:
        await conn.execute(
            text("UPDATE users SET password_hash = :pass_hash WHERE email = :email"),
            {"pass_hash": pass_hash, "email": "admin@alkhayma.com"},
        )
    print("Admin password reset successfully.")


if __name__ == "__main__":
    asyncio.run(main())

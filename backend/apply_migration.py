#!/usr/bin/env python
"""
Direct migration application script - apply schema
"""
import sys
import asyncio
from sqlalchemy import text, inspect
from app.core.database import AsyncSessionLocal, engine


async def apply_migration():
    async with AsyncSessionLocal() as db:
        try:
            # Check if migrations have been applied
            inspector = inspect(engine.sync_engine)
            tables = inspector.get_table_names()

            if "rooms" not in tables:
                print("⚠️  Rooms table not found. Applying Alembic migration...")
                # Try to run alembic upgrade
                import subprocess

                result = subprocess.run(
                    [sys.executable, "-m", "alembic", "upgrade", "head"],
                    cwd="/home/wego/Desktop/alkhayma-resort/backend",
                )
                if result.returncode != 0:
                    print("⚠️  Alembic upgrade attempt made but verify tables")

            # Check again
            inspector = inspect(engine.sync_engine)
            tables = inspector.get_table_names()

            if "rooms" in tables:
                print("✅ Rooms table exists")

                # Check if rating and review_count columns exist
                columns = [col["name"] for col in inspector.get_columns("rooms")]

                if "rating" not in columns:
                    await db.execute(
                        text(
                            """
                        ALTER TABLE rooms ADD COLUMN rating FLOAT DEFAULT 4.0 NOT NULL;
                    """
                        )
                    )
                    print("✅ Added rating column")

                if "review_count" not in columns:
                    await db.execute(
                        text(
                            """
                        ALTER TABLE rooms ADD COLUMN review_count INTEGER DEFAULT 0 NOT NULL;
                    """
                        )
                    )
                    print("✅ Added review_count column")

                await db.commit()
                print("✅ Table enhancement completed!")
            else:
                print("❌ Rooms table still does not exist after migration attempt")
                sys.exit(1)

        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback

            traceback.print_exc()
            await db.rollback()
            sys.exit(1)


if __name__ == "__main__":
    asyncio.run(apply_migration())

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base import BaseRepository
from app.models.product import Product

class ProductRepository(BaseRepository[Product]):
    def __init__(self, db: AsyncSession):
        super().__init__(Product, db)

    async def get_active_products(self, product_type: Optional[str] = None) -> List[Product]:
        query = select(Product).where(Product.is_active == True)
        if product_type:
            query = query.where(Product.type == product_type)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_by_slug(self, slug: str) -> Optional[Product]:
        result = await self.db.execute(select(Product).where(Product.slug == slug))
        return result.scalar_one_or_none()

from sqlalchemy import select, insert
from src.schemas.hotels import HotelCreateData, Hotel
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsORM


class HotelsRepository(BaseRepository):
    model = HotelsORM
    
    async def get_all(
            self, 
            title: str | None = None,
            location: str | None = None,
            limit: int = 3,
            offset: int = 0
        ):
        query = select(self.model)
        # Filters
        query = query.filter(self.model.title.icontains(title)) if title else query
        query = query.filter(self.model.location.icontains(location)) if location else query
        # LIMIT and OFFSET
        query = query.offset(offset).limit(limit)
        query_result = await self.session.execute(query)
        return query_result.scalars().all()


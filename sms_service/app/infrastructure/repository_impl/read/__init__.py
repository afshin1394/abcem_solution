from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Query
from math import ceil

from app.domain.entities import PaginatedResult


class BaseReadRepositoryImpl:


    def __init__(self,db : AsyncSession):
        super().__init__()
        self.db = db

    @staticmethod
    def apply_pagination(query: Query, page: Optional[int], page_size: Optional[int]) -> Query:
        """Apply pagination if page and page_size are provided."""
        if page is not None and page_size is not None:
            offset = (page - 1) * page_size
            query = query.offset(offset).limit(page_size)

        return query
    async def paginate_query(
        self,
        base_query: Query,
        model,
        page: Optional[int],
        page_size: Optional[int],
        map_func=None
    ) -> PaginatedResult:
        """Execute query with pagination and return paginated response."""

        # Apply pagination
        paginated_query = self.apply_pagination(base_query, page, page_size)

        # Execute paginated query
        result = await self.db.execute(paginated_query)
        records = result.scalars().all()

        # Execute total count query
        total_query = select(func.count()).select_from(model)
        total_result = await self.db.execute(total_query)
        total_items = total_result.scalar_one()

        # Map models to domain objects if mapper function provided
        if map_func:
            items = await map_func(records)
        else:
            items = records

        # Calculate total pages
        total_pages = ceil(total_items / page_size) if page and page_size else 1
        print(f'total_items {total_items}',flush=True)
        print(f'page_size {page_size}',flush=True)
        print(f'total_pages {total_pages}',flush=True)
        print(f'total_result {total_result}',flush=True)
        print(f'items {items}',flush=True)
        return PaginatedResult(
            items=items,
            page=page,
            page_size=page_size,
            total_items=total_items,
            total_pages=total_pages
        )

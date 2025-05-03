from typing import Generic, List, Optional, TypeVar

from pydantic.v1.generics import GenericModel

T = TypeVar('T')

class PaginatedResult(GenericModel, Generic[T]):
    items: List[T]
    page: Optional[int] = None
    page_size: Optional[int] = None
    total_items: Optional[int] = None
    total_pages: Optional[int] = None

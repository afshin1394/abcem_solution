from abc import ABC
from typing import List, Optional
from pydantic import BaseModel, Field




class Command(BaseModel):


    """
    A base class for commands with optional correlation ID and cache invalidation keys.

    Args:
        correlation_id (Optional[str]): An optional identifier for correlating commands.
        invalidate_cache_keys (List[str]): A list of cache keys to invalidate.
    """
    correlation_id: Optional[str] = Field(
        default=None,
        alias="correlationId",
        description="An optional identifier for correlating commands."
    )
    # invalidate_cache_keys: Optional[List[str]] = Field(
    #     ...,
    #     alias="invalidateCacheKeys",
    #     description="A list of cache keys to invalidate."
    # )

    class Config:
        """
        Configuration for the Command model.

        - allow_population_by_field_name: Allows population of the model using field names instead of aliases.
        - orm_mode: Enables compatibility with ORMs (if needed).
        - arbitrary_types_allowed: Allows arbitrary types (if needed).
        """
        populate_by_name = True
        from_attribute = True
        arbitrary_types_allowed = True

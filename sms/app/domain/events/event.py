
from abc import ABC

from pydantic import BaseModel, Field


class Event(BaseModel, ABC):
    """
    A base class for events.

    Args:
        correlation_id (str): An identifier to correlate events.
    """
    correlation_id: str = Field(
        ...,
        alias="correlationId",
        description="An identifier to correlate events."
    )



    class Config:
        """
        Configuration for the Event model.

        - allow_population_by_field_name: Allows population of the model using field names instead of aliases.
        - orm_mode: Enables compatibility with ORMs (if needed).
        - arbitrary_types_allowed: Allows arbitrary types (if needed).
        - use_enum_values: Serializes enums using their values.
        """
        populate_by_name = True
        from_attributes = True
        arbitrary_types_allowed = True
        use_enum_values = True




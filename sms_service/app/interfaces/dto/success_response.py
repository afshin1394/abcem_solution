from typing import Generic, TypeVar, Optional
from pydantic import Field, BaseModel, model_validator

# A type variable for the data we're returning
DataT = TypeVar("DataT")


class BaseSuccessResponse(BaseModel, Generic[DataT]):
    """
    A generic success response model with a default HTTP 200 status code
    and a 'result' that can be any type or model.
    """
    status_code: int = Field(200, description="HTTP status code, defaults to 200")
    latency: Optional[float] = Field(0,description="Latency (in seconds)")
    result: Optional[DataT] = Field(description="Actual data returned by the endpoint")
    page: Optional[int] = Field(None,description="page number")
    page_size: Optional[int] = Field(None,description="page size")
    total_items: Optional[int] = Field(None,description="total number of items")
    total_pages: Optional[int] = Field(None,description="total pages")

    @model_validator(mode='before')
    def remove_none_values(cls, values):
        # Remove fields with None values
        return {k: v for k, v in values.items() if v is not None}
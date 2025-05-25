from pydantic import BaseModel
import hashlib
import orjson


class Query(BaseModel):
    """
    Base class for all Queries in the CQRS pattern.
    """

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

    async def generate_cache_key(self) -> str:
        """Generate a hashed cache key for the query to reduce length and ensure uniqueness."""
        query_json = orjson.dumps(self.model_dump(), option=orjson.OPT_SORT_KEYS)
        query_hash = hashlib.sha256(query_json).hexdigest()  # Create SHA-256 hash
        return f"{self.__class__.__name__}:{query_hash}"

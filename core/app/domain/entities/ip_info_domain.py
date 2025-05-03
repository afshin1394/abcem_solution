from dataclasses import dataclass, field
from typing import Optional

@dataclass
class IPInfoDomain:
    ip: Optional[str] = None
    hostname: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    region: Optional[str] = None
    country: Optional[str] = None
    loc: Optional[str] = None
    org: Optional[str] = None
    postal: Optional[str] = None
    timezone: Optional[str] = None
    readme: Optional[str] = None

    def to_dict(self):
        """Convert dataclass instance to dictionary (like Pydantic's `.model_dump()`)."""
        return self.__dict__

    @staticmethod
    def example():
        """Returns an example instance similar to Pydantic's `json_schema_extra`."""
        return IPInfoDomain(
            ip="8.8.8.8",
            hostname="dns.google",
            city="Mountain View",
            state="California",
            region="North America",
            country="US",
            loc="37.3861,-122.0839",
            org="AS15169 Google LLC",
            postal="94043",
            timezone="America/Los_Angeles",
            readme="https://ipinfo.io/missingauth"
        )

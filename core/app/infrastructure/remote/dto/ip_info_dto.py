
from dataclasses import dataclass
from typing import Optional

@dataclass
class IpInfoDTO:
    ip: Optional[str]
    hostname: Optional[str]
    city: Optional[str]
    state: Optional[str]
    region: Optional[str]
    country: Optional[str]
    loc: Optional[str]
    org: Optional[str]
    postal: Optional[str]
    timezone: Optional[str]
    readme: Optional[str]

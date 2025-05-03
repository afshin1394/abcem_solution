from dataclasses import dataclass
from datetime import datetime

from pydantic import BaseModel

@dataclass
class DeviceInfoDomain:
    security_patch : datetime
    sdk : int
    os_version : int
    brand : str
    device : str
    hardware : str
    model : str
    walk_test_id : str

    def __repr__(self) -> str:
        return (
            f"DeviceInfoDomain(security_patch={self.security_patch!r}, "
            f"sdk={self.sdk!r}, os_version={self.os_version!r}, "
            f"brand={self.brand!r}, device={self.device!r}, "
            f"hardware={self.hardware!r}, model={self.model!r}, "
            f"walk_test_id={self.walk_test_id!r})"
        )

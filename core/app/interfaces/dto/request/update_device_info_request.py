from datetime import datetime

from pydantic import BaseModel, field_validator


class UpdateDeviceInfoRequest(BaseModel):
     walk_test_id : str
     security_patch : datetime
     sdk : int
     os_version : int
     brand : str
     device : str
     hardware : str
     model : str

     @field_validator("security_patch", mode="plain")
     def remove_timezone(cls, v):
         if isinstance(v, datetime) and v.tzinfo is not None:
             return v.replace(tzinfo=None)
         return v

     class Config:
             json_schema_extra = {
                 "example": {
                     "walk_test_id": "9f1c8a86-1d5e-4b5c-9f9a-6d3b8d0a9b1e",
                     "security_patch": "2025-03-16T12:34:56",
                     "sdk": 30,
                     "os_version": 11,
                     "brand": "ExampleBrand",
                     "device": "ExampleDevice",
                     "hardware": "ExampleHardware",
                     "model": "ExampleModel"
                 }
             }

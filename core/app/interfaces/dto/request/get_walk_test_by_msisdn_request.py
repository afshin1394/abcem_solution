from pydantic import BaseModel


class GetWalkTestByMSISDNRequest(BaseModel):
    msisdn: str

    class Config:
        json_schema_extra = {
            "msisdn": {
                "msisdn": "09351111111"
            },
        }

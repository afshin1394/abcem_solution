from pydantic import BaseModel, Field


class CreateUserRequest(BaseModel):
    name: str
    age: str
    gender: str

    class Config:
        json_schema_extra = {
            "name": {
                "name": "ali"
            },
            "age": {
                "age": "21"
            },
            "gender": {
                "gender": "male"
            }
        }

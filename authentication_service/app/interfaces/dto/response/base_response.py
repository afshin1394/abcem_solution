from abc import abstractproperty, abstractmethod
from typing import Any, Optional, TypeVar, Generic
from pydantic import BaseModel

R = TypeVar('R')


class BaseResponse(BaseModel, Generic[R]):
    result: Optional[R] = None
    status_code: int = 200
    message: str = "OK"



    def on_error(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        self.message = message

    class Config:
        arbitrary_types_allowed = True

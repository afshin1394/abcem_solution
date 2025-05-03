from pydantic import BaseModel


class GetNLastSmsRecordsRequest(BaseModel):
      page : int
      page_size : int
from datetime import datetime

from pydantic import BaseModel


class RawLog(BaseModel):
    timestamp: datetime
    hostname: str
    identifier: str
    message: str

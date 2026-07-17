from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from core.enums import EventSource, EventType, Severity


class Event(BaseModel):
    timestamp: datetime
    hostname: str

    source: EventSource
    event_type: EventType
    severity: Severity

    message: str

    attributes: dict[str, Any] = Field(default_factory=dict)
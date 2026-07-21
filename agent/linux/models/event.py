from datetime import datetime
from typing import Any
from uuid import UUID, uuid4
from pydantic import BaseModel, Field

from core.enums import EventSource, EventType, Severity


class Event(BaseModel):
    id: UUID = Field(default_factory=uuid4)

    timestamp: datetime
    hostname: str

    source: EventSource
    event_type: EventType
    severity: Severity

    message: str

    attributes: dict[str, Any] = Field(default_factory=dict)
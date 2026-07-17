from models import Event, RawLog
from core.enums import EventSource, EventType, Severity
from typing import Any

class SSHEventFactory:

    @staticmethod
    def create(
        *,
        log: RawLog,
        event_type: EventType,
        severity: Severity,
        attributes: dict,
    ) -> Event:

        return Event(
            timestamp=log.timestamp,
            hostname=log.hostname,
            source=EventSource.SSH,
            event_type=event_type,
            severity=severity,
            message=log.message,
            attributes=attributes,
        )
    
    @staticmethod
    def create_authentication_event(
        *,
        log: RawLog,
        event_type: EventType,
        severity: Severity,
        username: str,
        source_ip: str,
        port: int,
        extra_attributes: dict[str, Any] | None = None,
    ) -> Event:

        attributes = {
            "username": username,
            "source_ip": source_ip,
            "port": port,
        }

        if extra_attributes:
            attributes.update(extra_attributes)

        return SSHEventFactory.create(
            log=log,
            event_type=event_type,
            severity=severity,
            attributes=attributes,
        )
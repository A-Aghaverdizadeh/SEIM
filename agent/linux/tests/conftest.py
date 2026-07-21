from datetime import datetime

import pytest

from models.raw_log import RawLog
from models.event import Event
from core.enums import EventType, Severity

@pytest.fixture
def make_log():
    def _make_log(message: str):
        return RawLog(
            timestamp=datetime.now(),
            hostname="debian",
            identifier="sshd",
            message=message,
        )

    return _make_log

@pytest.fixture
def raw_log():
    return RawLog(
        timestamp=datetime.now(),
        hostname="debian",
        identifier="sshd",
        message="Test message",
    )

@pytest.fixture
def sample_event():

    return Event(
        timestamp=datetime.now(),
        hostname="debian",
        source="ssh",
        event_type=EventType.LOGIN_FAILED,
        severity=Severity.MEDIUM,
        message="Failed password for linuxguy",
        attributes={
            "username": "linuxguy",
            "source_ip": "::1",
        },
    )
import pytest

from datetime import datetime

from models.event import Event
from core.enums import EventType, Severity
from persistence.jsonl import JsonLinesRepository
from persistence.spool import EventSpool


@pytest.fixture
def spool(tmp_path):

    repository = JsonLinesRepository(
        tmp_path / "events.jsonl"
    )

    return EventSpool(repository)

def test_enqueue_adds_event(
    spool,
    sample_event,
):

    spool.enqueue(sample_event)

    assert spool.size() == 1

def test_dequeue_returns_event(
    spool,
    sample_event,
):

    spool.enqueue(sample_event)

    event = spool.dequeue()

    assert event == sample_event

def test_acknowledge_removes_event(
    spool,
    sample_event,
):

    spool.enqueue(sample_event)

    event = spool.dequeue()

    spool.acknowledge(event)

    assert spool.repository.load() == []

def test_recovers_events_after_restart(
    tmp_path,
    sample_event,
):

    repository = JsonLinesRepository(
        tmp_path / "events.jsonl"
    )

    spool = EventSpool(repository)

    spool.enqueue(sample_event)

    #
    # Simulate agent restart
    #

    spool = EventSpool(repository)

    assert spool.size() == 1

    event = spool.dequeue()

    assert event == sample_event

def test_recovers_multiple_events(tmp_path):

    repository = JsonLinesRepository(
        tmp_path / "events.jsonl"
    )

    spool = EventSpool(repository)

    for i in range(10):

        spool.enqueue(
            Event(
                timestamp=datetime.now(),
                hostname="host",
                source="ssh",
                event_type=EventType.LOGIN_FAILED,
                severity=Severity.MEDIUM,
                message=str(i),
                attributes={}
            )
        )

    spool = EventSpool(repository)

    assert spool.size() == 10

def test_empty_repository_loads_no_events(tmp_path):

    repository = JsonLinesRepository(
        tmp_path / "events.jsonl"
    )

    spool = EventSpool(repository)

    assert spool.size() == 0
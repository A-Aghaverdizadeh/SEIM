import pytest
from datetime import datetime
from pathlib import Path

from models.event import Event
from core.enums import EventType, Severity
from persistence.jsonl import JsonLinesRepository


@pytest.fixture
def repository(tmp_path):

    path = tmp_path / "events.jsonl"

    return JsonLinesRepository(path)


@pytest.fixture
def sample_event():

    return Event(
        timestamp=datetime.now(),
        hostname="debian",
        source="ssh",
        event_type=EventType.LOGIN_FAILED,
        severity=Severity.MEDIUM,
        message="Failed password",
        attributes={
            "username": "linuxguy"
        }
    )

def test_save_creates_file(
    repository,
    sample_event,
):

    repository.save(sample_event)

    events = repository.load()

    assert len(events) == 1

def test_load_returns_saved_event(
    repository,
    sample_event,
):

    repository.save(sample_event)

    loaded = repository.load()

    assert loaded[0] == sample_event

def test_delete_removes_event(
    repository,         
    sample_event,
):

    repository.save(sample_event)

    repository.delete(sample_event.id)

    assert repository.load() == []

def test_load_multiple_events(repository):

    events = []

    for i in range(5):

        event = Event(
            timestamp=datetime.now(),
            hostname="host",
            source="ssh",
            event_type=EventType.LOGIN_FAILED,
            severity=Severity.MEDIUM,
            message=f"event {i}",
            attributes={}
        )

        repository.save(event)

        events.append(event)

    loaded = repository.load()

    assert loaded == events

def test_delete_only_target_event(repository):

    events = []

    for i in range(3):

        event = Event(
            timestamp=datetime.now(),
            hostname="host",
            source="ssh",
            event_type=EventType.LOGIN_FAILED,
            severity=Severity.MEDIUM,
            message=str(i),
            attributes={}
        )

        repository.save(event)

        events.append(event)

    repository.delete(events[1].id)

    loaded = repository.load()

    assert len(loaded) == 2
    assert events[1] not in loaded
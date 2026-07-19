from core.enums import (
    EventSource,
    EventType,
    Severity,
)

from core.event_factory import SSHEventFactory


class TestSSHEventFactory:

    def test_create_authentication_event(self, raw_log):

        event = SSHEventFactory.create_authentication_event(
            log=raw_log,
            event_type=EventType.LOGIN_FAILED,
            severity=Severity.MEDIUM,
            username="linuxguy",
            source_ip="192.168.1.10",
            port=22,
        )

        assert event.timestamp == raw_log.timestamp

        assert event.hostname == raw_log.hostname

        assert event.message == raw_log.message

        assert event.source == EventSource.SSH

        assert event.event_type == EventType.LOGIN_FAILED

        assert event.severity == Severity.MEDIUM

        assert event.attributes["username"] == "linuxguy"

        assert event.attributes["source_ip"] == "192.168.1.10"

        assert event.attributes["port"] == 22

    def test_create_authentication_event_with_extra_attributes(self, raw_log):

        event = SSHEventFactory.create_authentication_event(
            log=raw_log,
            event_type=EventType.PUBLICKEY_LOGIN,
            severity=Severity.LOW,
            username="linuxguy",
            source_ip="192.168.1.10",
            port=22,
            extra_attributes={
                "authentication_method": "publickey",
                "algorithm": "RSA",
            },
        )

        assert event.attributes["authentication_method"] == "publickey"

        assert event.attributes["algorithm"] == "RSA"

    def test_create_preserves_custom_attributes(self, raw_log):

        attributes = {
            "test": "value",
            "number": 100,
        }

        event = SSHEventFactory.create(
            log=raw_log,
            event_type=EventType.LOGIN_SUCCESS,
            severity=Severity.LOW,
            attributes=attributes,
        )

        assert event.attributes == attributes

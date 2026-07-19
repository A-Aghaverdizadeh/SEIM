import pytest

from core.enums import EventType
from parsers.ssh_rules.failed_login import FailedLoginRule

class TestFailedLoginRule:

    @pytest.mark.parametrize(
        "message,username,ip,port",
        [
            (
                "Failed password for linuxguy from 192.168.1.10 port 22 ssh2",
                "linuxguy",
                "192.168.1.10",
                22,
            ),
            (
                "Failed password for root from 10.0.0.5 port 2222 ssh2",
                "root",
                "10.0.0.5",
                2222,
            ),
        ],
    )
    
    def test_valid_messages(
        self,
        make_log,
        message,
        username,
        ip,
        port,
    ):
        parser = FailedLoginRule()

        event = parser.parse(make_log(message))

        assert event is not None
        assert event.event_type == EventType.LOGIN_FAILED

        assert event.attributes["username"] == username
        assert event.attributes["source_ip"] == ip
        assert event.attributes["port"] == port

    @pytest.mark.parametrize(
        "message",
        [
            "Accepted password for linuxguy from 192.168.1.10 port 22 ssh2",
            "Invalid user admin from 192.168.1.10 port 22",
            "Timeout before authentication for connection from ::1 to ::1, pid = 1234",
            "Random text",
            "",
        ],
    )

    def test_invalid_messages(self, make_log, message):

        parser = FailedLoginRule()

        assert parser.parse(make_log(message)) is None
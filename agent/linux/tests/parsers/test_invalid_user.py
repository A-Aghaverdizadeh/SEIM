import pytest

from core.enums import EventType
from parsers.ssh_rules.invalid_user import InvalidUserRule


class TestInvalidUserRule:

    @pytest.mark.parametrize(
        "message,username,ip,port",
        [
            (
                "Invalid user admin from 192.168.1.100 port 50124",
                "admin",
                "192.168.1.100",
                50124,
            ),
            (
                "Invalid user oracle from 10.0.0.2 port 2222",
                "oracle",
                "10.0.0.2",
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

        parser = InvalidUserRule()

        event = parser.parse(make_log(message))

        assert event is not None
        assert event.event_type == EventType.INVALID_USER

        assert event.attributes["username"] == username
        assert event.attributes["source_ip"] == ip
        assert event.attributes["port"] == port

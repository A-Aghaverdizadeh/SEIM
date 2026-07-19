import pytest

from core.enums import EventType
from parsers.ssh_rules.authentication_timeout import AuthenticationTimeoutRule


class TestAuthenticationTimeoutRule:
    @pytest.mark.parametrize(
        "message,src,dst,pid",
        [
            (
                "Timeout before authentication for connection from ::1 to ::1, pid = 1234",
                "::1",
                "::1",
                1234,
            ),
        ],
    )
    def test_valid_messages(
        self,
        make_log,
        message,
        src,
        dst,
        pid,
    ):
        parser = AuthenticationTimeoutRule()

        event = parser.parse(make_log(message))

        assert event is not None
        assert event.event_type == EventType.AUTHENTICATION_TIMEOUT

        assert event.attributes["source_ip"] == src
        assert event.attributes["destination_ip"] == dst
        assert event.attributes["pid"] == pid
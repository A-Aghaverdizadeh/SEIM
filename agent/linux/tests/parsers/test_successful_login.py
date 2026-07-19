import pytest

from core.enums import EventType
from parsers.ssh_rules.accepted_login import AcceptedLoginRule

class TestAcceptedLoginRule:

    @pytest.mark.parametrize(
        "message,username,ip,port",
        [
            (
                "Accepted password for linuxguy from 192.168.1.10 port 22 ssh2",
                "linuxguy",
                "192.168.1.10",
                22,
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
        parser = AcceptedLoginRule()

        event = parser.parse(make_log(message))

        assert event is not None
        assert event.event_type == EventType.LOGIN_SUCCESS

        assert event.attributes["username"] == username
        assert event.attributes["source_ip"] == ip
        assert event.attributes["port"] == port

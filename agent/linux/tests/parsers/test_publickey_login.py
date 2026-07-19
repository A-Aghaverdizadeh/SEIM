import pytest

from core.enums import EventType
from parsers.ssh_rules.publickey_login import PublickeyLoginRule


class TestPublickeyLoginRule:

    @pytest.mark.parametrize(
        "message,username,ip,port",
        [
            (
                "Accepted publickey for linuxguy from 192.168.1.10 port 22 ssh2",
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
        parser = PublickeyLoginRule()

        event = parser.parse(make_log(message))

        assert event is not None
        assert event.event_type == EventType.PUBLICKEY_LOGIN

        assert event.attributes["username"] == username
        assert event.attributes["source_ip"] == ip
        assert event.attributes["port"] == port
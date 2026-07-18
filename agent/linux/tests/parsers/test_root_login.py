import pytest

from core.enums import EventType
from parsers.ssh_rules.root_login import RootLoginRule


class TestRootLoginRule:

    @pytest.mark.parametrize(
        "message,ip,port",
        [
            (
                "Accepted password for root from 192.168.1.15 port 22 ssh2",
                "192.168.1.15",
                22,
            ),
            (
                "Accepted password for root from 10.10.10.5 port 2222 ssh2",
                "10.10.10.5",
                2222,
            ),
        ],
    )

    def test_valid_messages(
        self,
        make_log,
        message,
        ip,
        port,
    ):

        parser = RootLoginRule()

        event = parser.parse(make_log(message))

        assert event is not None
        assert event.event_type == EventType.ROOT_LOGIN

        assert event.attributes["source_ip"] == ip
        assert event.attributes["port"] == port

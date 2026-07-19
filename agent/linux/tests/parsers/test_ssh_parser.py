from core.enums import EventType
from models.raw_log import RawLog
from parsers.ssh import SSHParser

from datetime import datetime


class TestSSHParser:

    def test_failed_login(self):

        parser = SSHParser()

        log = RawLog(
            timestamp=datetime.now(),
            hostname="debian",
            identifier="sshd",
            message="Failed password for linuxguy from 192.168.1.10 port 22 ssh2",
        )

        event = parser.parse(log)

        assert event is not None
        assert event.event_type == EventType.LOGIN_FAILED
    
    def test_unknown_message(self):

        parser = SSHParser()

        log = RawLog(
            timestamp=datetime.now(),
            hostname="debian",
            identifier="sshd",
            message="Something completely random",
        )

        assert parser.parse(log) is None
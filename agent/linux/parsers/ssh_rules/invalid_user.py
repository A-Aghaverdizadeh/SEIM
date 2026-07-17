import re

from models import RawLog
from .base import BaseSSHRule
from core.enums import EventType, Severity
from core.event_factory import SSHEventFactory

INVALID_USER = re.compile(
    r"Invalid user (?P<username>\S+) from (?P<ip>\S+) port (?P<port>\d+)"
)
    

class InvalidUserRule(BaseSSHRule):

    def parse(self, log: RawLog):

        match = INVALID_USER.search(log.message)

        if not match:
            return None

        return SSHEventFactory.create_authentication_event(
            log=log,
            event_type=EventType.INVALID_USER,
            severity=Severity.MEDIUM,
            username=match.group("username"),
            source_ip=match.group("ip"),
            port=int(match.group("port")),
        )
    
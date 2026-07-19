import re

from models.raw_log import RawLog
from .base import BaseSSHRule
from core.enums import EventType, Severity
from core.event_factory import SSHEventFactory

ROOT_LOGIN = re.compile(
    r"Accepted password for (?P<username>\S+) from (?P<ip>\S+) port (?P<port>\d+)"
)
    

class RootLoginRule(BaseSSHRule):

    def parse(self, log: RawLog):

        match = ROOT_LOGIN.search(log.message)

        if not match:
            return None

        return SSHEventFactory.create_authentication_event(
            log=log,
            event_type=EventType.ROOT_LOGIN,
            severity=Severity.HIGH,
            username="root",
            source_ip=match.group("ip"),
            port=int(match.group("port")),
        )
    
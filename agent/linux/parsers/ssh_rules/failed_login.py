import re

from models.raw_log import RawLog
from .base import BaseSSHRule
from core.enums import EventType, Severity
from core.event_factory import SSHEventFactory

FAILED_LOGIN = re.compile(
    r"Failed password for (?P<username>\S+) from (?P<ip>\S+) port (?P<port>\d+)"
)


class FailedLoginRule(BaseSSHRule):

    def parse(self, log: RawLog):

        match = FAILED_LOGIN.search(log.message)

        if not match:
            return None

        return SSHEventFactory.create_authentication_event(
            log=log,
            event_type=EventType.LOGIN_FAILED,
            severity=Severity.MEDIUM,
            username=match.group("username"),
            source_ip=match.group("ip"),
            port=int(match.group("port")),
        )
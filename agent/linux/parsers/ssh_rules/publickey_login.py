import re

from models.raw_log import RawLog
from .base import BaseSSHRule
from core.enums import EventType, Severity
from core.event_factory import SSHEventFactory

PUBLICKEY_LOGIN = re.compile(
    r"Accepted publickey for (?P<username>\S+) from (?P<ip>\S+) port (?P<port>\d+)"
)


class PublickeyLoginRule(BaseSSHRule):

    def parse(self, log: RawLog):

        match = PUBLICKEY_LOGIN.search(log.message)

        if not match:
            return None

        return SSHEventFactory.create_authentication_event(
            log=log,
            event_type=EventType.PUBLICKEY_LOGIN,
            severity=Severity.LOW,
            username=match.group("username"),
            source_ip=match.group("ip"),
            port=int(match.group("port")),
            # extra_attributes={
            #     "authentication_method": "publickey"
            # }
        )
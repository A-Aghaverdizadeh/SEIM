from parsers.ssh_rules.base import BaseSSHRule
from core.enums import EventType, Severity
from core.event_factory import SSHEventFactory

import re

AUTHENTICATION_TIMEOUT_PATTERN = re.compile(
    r"Timeout before authentication for connection from (?P<source_ip>\S+) to (?P<destination_ip>\S+), pid = (?P<pid>\d+)"
)


class AuthenticationTimeoutRule(BaseSSHRule):

    def parse(self, log):

        match = AUTHENTICATION_TIMEOUT_PATTERN.search(log.message)

        if not match:
            return None

        return SSHEventFactory.create(
            log=log,
            event_type=EventType.AUTHENTICATION_TIMEOUT,
            severity=Severity.LOW,
            attributes={
                "source_ip": match.group("source_ip"),
                "destination_ip": match.group("destination_ip"),
                "pid": int(match.group("pid")),
            },
        )
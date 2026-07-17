from models import RawLog, Event
from .base import BaseParser
from .ssh_rules import failed_login, accepted_login, invalid_user, publickey_login, root_login, authentication_timeout

class SSHParser(BaseParser):

    def __init__(self):

        self.rules = [
            failed_login.FailedLoginRule(),
            accepted_login.AcceptedLoginRule(),
            invalid_user.InvalidUserRule(),
            publickey_login.PublickeyLoginRule(),
            root_login.RootLoginRule(),
            authentication_timeout.AuthenticationTimeoutRule(),
        ]

    def parse(self, log: RawLog) -> Event | None:

        for rule in self.rules:

            event = rule.parse(log)

            if event is not None:
                return event

        return None
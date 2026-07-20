from abc import ABC, abstractmethod

from models.event import Event


class BaseTransport(ABC):
    """
    Base interface for event transport mechanisms.

    Responsible for delivering normalized security events
    from the agent to external SIEM components.
    """

    @abstractmethod
    def send(self, event: Event) -> None:
        """
        Send a security event.
        """
        pass
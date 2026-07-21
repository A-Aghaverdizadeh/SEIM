from abc import ABC, abstractmethod

from models.event import Event


class EventRepository(ABC):
    """
    Defines the persistence contract for security events.
    """

    @abstractmethod
    def save(self, event: Event) -> None:
        """
        Persist an event.
        """
        ...

    @abstractmethod
    def delete(self, event_id) -> None:
        """
        Remove an event.
        """
        ...

    @abstractmethod
    def load(self) -> list[Event]:
        """
        Load all persisted events.
        """
        ...
from queue import Queue

from models.event import Event
from persistence.repository import EventRepository


class EventSpool:
    """
    Persistent event queue.

    Every queued event is written to disk before entering the
    in-memory queue, allowing the agent to recover events after
    restarts or crashes.
    """

    def __init__(self, repository: EventRepository):

        self.repository = repository
        self.queue = Queue()

        # Recover persisted events.
        for event in repository.load():
            self.queue.put(event)

    def enqueue(self, event: Event) -> None:

        self.repository.save(event)
        self.queue.put(event)

    def dequeue(self) -> Event:

        return self.queue.get()

    def acknowledge(self, event: Event) -> None:

        self.repository.delete(event.id)
        self.queue.task_done()

    def size(self) -> int:

        return self.queue.qsize()
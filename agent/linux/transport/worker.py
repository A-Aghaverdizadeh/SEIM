import threading

from models.event import Event
from transport.base import BaseTransport
from event_queue.event_queue import EventQueue


class TransportWorker(threading.Thread):
    """
    Background worker responsible for sending
    queued events to the SIEM server.
    """

    def __init__(
        self,
        queue: EventQueue,
        transport: BaseTransport,
        retry_policy,
    ):

        super().__init__(
            daemon=True
        )

        self.queue = queue
        self.transport = transport
        self.retry_policy = retry_policy


    def run(self):

        while True:

            event = self.queue.get()

            try:

                self.retry_policy.execute(
                    self.transport.send,
                    event,
                )

                self.queue.task_done()

            except Exception as exc:

                print(
                    f"Event permanently failed: {exc}"
                )

                self.queue.task_done()
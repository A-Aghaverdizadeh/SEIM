import threading

from transport.base import BaseTransport
from persistence.spool import EventSpool


class TransportWorker(threading.Thread):
    """
    Background worker responsible for sending
    queued events to the SIEM server.
    """

    def __init__(
        self,
        spool: EventSpool,
        transport: BaseTransport,
        retry_policy,
    ):

        super().__init__(
            daemon=True
        )

        self.spool = spool
        self.transport = transport
        self.retry_policy = retry_policy


    def run(self):

        while True:

            event = self.spool.dequeue()

            try:

                self.retry_policy.execute(
                    self.transport.send,
                    event,
                )

                self.spool.acknowledge(event)

            except Exception as exc:

                print(
                    f"Failed to deliver event: {exc}"
                )
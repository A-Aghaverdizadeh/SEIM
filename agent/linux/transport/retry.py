import time

from models.event import Event


class RetryPolicy:
    """
    Simple fixed-delay retry policy.

    Determines how many retry attempts should be made
    and how long to wait between attempts.
    """

    def __init__(
        self,
        max_attempts: int = 3,
        delay: int = 2,
    ):
        self.max_attempts = max_attempts
        self.delay = delay

    def execute(self, func, event: Event):
        """
        Execute a transport operation with retry support.
        """

        last_exception = None

        for attempt in range(1, self.max_attempts + 1):

            try:
                return func(event)

            except Exception as exc:

                last_exception = exc

                print(
                    f"[Retry {attempt}/{self.max_attempts}] "
                    f"{exc}"
                )

                if attempt < self.max_attempts:
                    time.sleep(self.delay)

        raise last_exception
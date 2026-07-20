import httpx

from models.event import Event
from transport.base import BaseTransport


class HTTPTransport(BaseTransport):
    """
    Sends security events to a SIEM server using HTTP POST.
    """

    def __init__(
        self,
        endpoint: str,
        timeout: int = 5
    ):

        self.endpoint = endpoint
        self.timeout = timeout


    def send(
        self,
        event: Event
    ) -> None:

        response = httpx.post(
            self.endpoint,
            json=event.model_dump(
                mode="json"
            ),
            timeout=self.timeout
        )

        response.raise_for_status()
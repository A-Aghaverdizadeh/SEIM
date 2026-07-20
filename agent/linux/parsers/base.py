from abc import ABC, abstractmethod

from models.event import Event
from models.raw_log import RawLog


class BaseParser(ABC):
    """
    Base interface for all log parsers.

    Parsers receive normalized RawLog objects and attempt
    to convert them into security Events.

    A parser should return:
        - Event: if it recognizes and processes the log
        - None: if the log does not belong to this parser
    """

    @abstractmethod
    def parse(self, log: RawLog) -> Event | None:
        pass
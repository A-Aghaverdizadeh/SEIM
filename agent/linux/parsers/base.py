from abc import ABC, abstractmethod

from models.event import Event
from models.raw_log import RawLog


class BaseParser(ABC):

    @abstractmethod
    def parse(self, log: RawLog) -> Event | None:
        pass
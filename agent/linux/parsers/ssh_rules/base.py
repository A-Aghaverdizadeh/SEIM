from abc import ABC, abstractmethod

from models import RawLog, Event


class BaseSSHRule(ABC):

    @abstractmethod
    def parse(self, log: RawLog) -> Event | None:
        pass
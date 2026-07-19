from collections.abc import Iterator

from models.event import Event
from models.raw_log import RawLog


class AgentPipeline:

    def __init__(self, collector, parser):
        self.collector = collector
        self.parser = parser

    def process(self) -> Iterator[Event]:

        for log in self.collector.collect():

            event = self.parser.parse(log)

            if event is not None:
                yield event
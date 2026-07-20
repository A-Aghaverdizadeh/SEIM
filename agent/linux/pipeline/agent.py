from collections.abc import Iterator

from models.event import Event
from models.raw_log import RawLog


class AgentPipeline:

    def __init__(self, collector, parsers: list):
        self.collector = collector
        self.parsers = parsers

    def process(self) -> Iterator[Event]:

        for log in self.collector.collect():

            for parser in self.parsers:

                event = parser.parse(log)

                if event is not None:
                    yield event
                    break
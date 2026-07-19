from datetime import datetime

from core.enums import EventType
from models.raw_log import RawLog
from parsers.ssh import SSHParser
from pipeline.agent import AgentPipeline


# class TestLinuxPipeline:

#     def test_failed_login_pipeline(self):

#         parser = SSHParser()

#         log = RawLog(
#             timestamp=datetime.now(),
#             hostname="debian",
#             identifier="sshd",
#             message="Failed password for linuxguy from 192.168.1.10 port 22 ssh2",
#         )

#         event = parser.parse(log)

#         assert event is not None
#         assert event.event_type == EventType.LOGIN_FAILED
#         assert event.attributes["username"] == "linuxguy"

#     def test_multiple_logs(self):

#         parser = SSHParser()

#         logs = [
#             RawLog(
#                 timestamp=datetime.now(),
#                 hostname="debian",
#                 identifier="sshd",
#                 message="Failed password for admin from 10.0.0.1 port 22 ssh2",
#             ),
#             RawLog(
#                 timestamp=datetime.now(),
#                 hostname="debian",
#                 identifier="sshd",
#                 message="Accepted password for linuxguy from 10.0.0.2 port 22 ssh2",
#             ),
#         ]

#         events = []

#         for log in logs:
#             event = parser.parse(log)
#             if event:
#                 events.append(event)

#         assert len(events) == 2
#         assert events[0].event_type == EventType.LOGIN_FAILED
#         assert events[1].event_type == EventType.LOGIN_SUCCESS

class TestAgentPipeline:

    def test_process_events(self):

        pipeline = AgentPipeline(
            collector=FakeCollector(),
            parser=SSHParser(),
        )

        events = list(pipeline.process())

        assert len(events) == 2

        assert events[0].event_type == EventType.LOGIN_FAILED

        assert events[1].event_type == EventType.LOGIN_SUCCESS

class FakeCollector:

    def collect(self):

        yield RawLog(
            timestamp=datetime.now(),
            hostname="debian",
            identifier="sshd",
            message="Failed password for linuxguy from 192.168.1.10 port 22 ssh2",
        )

        yield RawLog(
            timestamp=datetime.now(),
            hostname="debian",
            identifier="sshd",
            message="Accepted password for linuxguy from 192.168.1.10 port 22 ssh2",
        )

class EmptyCollector:

    def collect(self):
        yield from ()

    def test_empty_collector(self):

        pipeline = AgentPipeline(
            collector=EmptyCollector(),
            parser=SSHParser(),
        )

        events = list(pipeline.process())

        assert events == []
    
class UnknownCollector:

    def collect(self):

        yield RawLog(
            timestamp=datetime.now(),
            hostname="debian",
            identifier="sshd",
            message="Completely random message",
        )

    def test_unknown_logs_are_ignored(self):

        pipeline = AgentPipeline(
            collector=UnknownCollector(),
            parser=SSHParser(),
        )

        events = list(pipeline.process())

        assert len(events) == 0


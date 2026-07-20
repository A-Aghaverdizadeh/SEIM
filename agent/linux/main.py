from collectors.journal import JournalCollector
from parsers.ssh import SSHParser
from pipeline.agent import AgentPipeline
from transport import HTTPTransport
from event_queue.event_queue import EventQueue
from transport.worker import TransportWorker
from transport.retry import RetryPolicy

collector = JournalCollector()
# parser = SSHParser()


pipeline = AgentPipeline(
    collector=collector,
    parsers=[
        SSHParser(),
    ]
)

event_queue = EventQueue()

# for event in pipeline.process():

#     # print(event.to_json())
#     print(print(event.model_dump_json(indent=2)))

transport = HTTPTransport(
    endpoint="http://localhost:8000/events"
)

retry_policy = RetryPolicy(
    max_attempts=3,
    delay=2,
)

worker = TransportWorker(
    queue=event_queue,
    transport=transport,
    retry_policy=retry_policy,
)


worker.start()

for event in pipeline.process():
    
    print(event.model_dump_json(indent=2))
    event_queue.put(event)
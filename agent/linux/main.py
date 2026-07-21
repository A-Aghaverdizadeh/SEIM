from pathlib import Path
from collectors.journal import JournalCollector
from parsers.ssh import SSHParser
from pipeline.agent import AgentPipeline
from transport import HTTPTransport
from persistence.spool import EventSpool
from persistence.jsonl import JsonLinesRepository 
from transport.worker import TransportWorker
from transport.retry import RetryPolicy

collector = JournalCollector()


pipeline = AgentPipeline(
    collector=collector,
    parsers=[
        SSHParser(),
    ]
)

repository = JsonLinesRepository(
    Path("queue/events.jsonl")
)

spool = EventSpool(repository)

transport = HTTPTransport(
    endpoint="http://localhost:8000/events"
)

retry_policy = RetryPolicy(
    max_attempts=3,
    delay=2,
)

worker = TransportWorker(
    spool=spool,
    transport=transport,
    retry_policy=retry_policy,
)


worker.start()

for event in pipeline.process():
    
    print(event.model_dump_json(indent=2))
    spool.enqueue(event)
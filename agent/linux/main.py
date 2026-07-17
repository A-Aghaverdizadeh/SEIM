from collectors.journal import JournalCollector
from parsers.ssh import SSHParser


collector = JournalCollector()
parser = SSHParser()


for log in collector.collect():

    event = parser.parse(log)

    if event is None:
        continue

    print(event.model_dump_json(indent=2))
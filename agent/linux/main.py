from collectors.journal import JournalCollector
from parsers.ssh import SSHParser
from pipeline.agent import AgentPipeline

collector = JournalCollector()
parser = SSHParser()


pipeline = AgentPipeline(
    collector=collector,
    parser=parser,
)

for event in pipeline.process():

    # print(event.to_json())
    print(print(event.model_dump_json(indent=2)))
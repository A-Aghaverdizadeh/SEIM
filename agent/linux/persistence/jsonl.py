from pathlib import Path

from models.event import Event
from persistence.repository import EventRepository


class JsonLinesRepository(EventRepository):

    def __init__(self, path: Path):

        self.path = path

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.path.touch(
            exist_ok=True
        )

    def save(self, event: Event) -> None:

        with self.path.open(
            "a",
            encoding="utf-8"
        ) as file:

            file.write(
                event.model_dump_json()
            )

            file.write("\n")

    def load(self) -> list[Event]:

        events = []

        with self.path.open(
            encoding="utf-8"
        ) as file:

            for line in file:

                line = line.strip()

                if not line:
                    continue

                events.append(
                    Event.model_validate_json(
                        line
                    )
                )

        return events
    
    def delete(self, event_id) -> None:

        events = self.load()

        with self.path.open(
            "w",
            encoding="utf-8"
        ) as file:

            for event in events:

                if event.id == event_id:
                    continue

                file.write(
                    event.model_dump_json()
                )

                file.write("\n")
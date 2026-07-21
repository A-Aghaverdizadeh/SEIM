from queue import Queue
from models.event import Event


class EventQueue:
    """
    Thread-safe queue for buffering generated security events.

    Decouples event generation from event transmission.
    """

    def __init__(self):
        self.queue = Queue()


    def put(self, event: Event):
        self.queue.put(event)


    def get(self) -> Event:
        return self.queue.get()


    def size(self):
        return self.queue.qsize()
    
    def task_done(self):
        self.queue.task_done()
    
    def join(self):
        self.queue.join()

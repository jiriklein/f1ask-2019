from queue import Queue, Empty
from threading import Event
from typing import Any


def handle_timeout(
    _q: Queue, event: Event, block: bool = True, timeout: float = 10.0
) -> Any:
    try:
        return _q.get(block, timeout)
    except Empty:
        if event.is_set():
            print("Event set. Closing.")

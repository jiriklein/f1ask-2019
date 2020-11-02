from queue import Queue
from typing import Iterable
from threading import Event


class F1Producer:
    _QUEUE_GET_TIMEOUT = 5.0

    def __init__(
        self,
        input_queues: Iterable[Queue],
        thread_end_event: Event,
        strategy: str = None,
    ):
        self._queues = input_queues
        self._end_event = thread_end_event
        self.product_messages = 0
        self.producer_strategy = strategy

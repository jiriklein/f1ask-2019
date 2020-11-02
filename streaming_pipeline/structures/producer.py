from queue import Queue
from typing import Iterable, Callable
from threading import Event


class F1Processor:
    _QUEUE_GET_TIMEOUT = 5.0

    def __init__(
        self,
        input_queue: Queue,
        output_queues: Iterable[Queue],
        thread_end_event: Event,
        strategy: Callable = None,
    ):
        self._input_queue = input_queue
        self._output_queues = output_queues
        self._end_event = thread_end_event
        self.processed_messages = 0
        self.strategy = strategy

    def produce(self):
        raw_pkt = self._input_queue.get(block=True, timeout=self._QUEUE_GET_TIMEOUT)
        if self.strategy:
            for _q in self._output_queues:
                _q.put(self.strategy(raw_pkt))
        else:
            # just write to file
            pass

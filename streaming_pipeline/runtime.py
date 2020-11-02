from queue import Queue
from threading import Event, Thread
from typing import Iterable


from streaming_pipeline.receiver import F1Receiver


def run():
    packet_queues = [Queue()]
    thread_end_event = Event()
    receiver = F1Receiver(
        output_queues=packet_queues, thread_end_event=thread_end_event
    )

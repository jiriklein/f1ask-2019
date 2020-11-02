from queue import Queue
from threading import Event, Thread
from typing import Iterable


from streaming_pipeline.receiver import F1Receiver


def run(shared_queue: Queue, end_event: Event):
    receiver = F1Receiver(output_queues=shared_queue, thread_end_event=end_event)
    receiver_thread = Thread(target=receiver.listen)

    receiver.connect()
    receiver_thread.start()

    while not end_event.is_set():
        try:
            if input().lower() == "end":
                end_event.set()
        except Exception as e:
            print(e)
            end_event.set()
        finally:
            receiver_thread.join()

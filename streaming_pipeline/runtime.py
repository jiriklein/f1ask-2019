from queue import Queue
from threading import Event, Thread
from time import sleep


from streaming_pipeline.receiver import F1Receiver
from streaming_pipeline.producer import F1Processor


def run(shared_queue: Queue, output_queue: Queue, end_event: Event):
    receiver = F1Receiver(output_queue=shared_queue, thread_end_event=end_event)
    receiver_thread = Thread(target=receiver.listen, daemon=True)

    producer = F1Processor(
        input_queue=shared_queue,
        output_queues=[output_queue],
        thread_end_event=end_event,
        strategy=F1Processor.speed_only,
    )
    producer_thread = Thread(target=producer.produce, args=(), daemon=True)

    receiver.connect()
    receiver_thread.start()
    producer_thread.start()

    while not end_event.is_set():
        try:
            sleep(1000)
        except KeyboardInterrupt:
            end_event.set()
        finally:
            receiver_thread.join()

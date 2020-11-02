from queue import Queue
from threading import Event, Thread

from flask import Flask

from streaming_pipeline.runtime import run

app = Flask(__name__)
shared_event = Event()
shared_queues = [Queue()]


@app.route("/")
def hello_world():
    return "Hello World!"


@app.route("/kill")
def kill_stream():
    shared_event.set()
    return "Set the event to kill stream."


if __name__ == "__main__":
    runtime = Thread(
        target=run,
        args=(
            shared_queues,
            shared_event,
        ),
        daemon=True,
    )
    runtime.start()

    app.run()

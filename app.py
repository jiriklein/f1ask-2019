from queue import Queue
from threading import Event, Thread

from flask import Flask, render_template
from flask_socketio import SocketIO

from streaming_pipeline.runtime import run
from streaming_pipeline.utils import handle_timeout

app = Flask(__name__)
app.config["DEBUG"] = True
socket_io = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)

shared_event = Event()
shared_queue = Queue()
production_queue = Queue()

thread = Thread()
emission_thread = Thread()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/kill")
def kill_stream():
    shared_event.set()
    return "Set the event to kill stream."


def produce_speed():
    while not shared_event.isSet():
        global production_queue
        pkt = handle_timeout(production_queue, shared_event)
        if pkt:
            socket_io.emit("f1", {"data": pkt}, namespace="/test")


@socket_io.on("connect", namespace="/test")
def test_connect():
    # need visibility of the global thread object
    global thread, emission_thread
    print("Client connected")

    if not thread.isAlive():
        print("Starting Thread")
        thread = socket_io.start_background_task(
            run, shared_queue, production_queue, shared_event
        )
        emission_thread = socket_io.start_background_task(produce_speed)


if __name__ == "__main__":
    socket_io.run(app=app)

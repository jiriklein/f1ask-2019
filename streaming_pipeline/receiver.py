from queue import Queue
import socket
import struct
from threading import Event

from streaming_pipeline.structures.packets import PacketHeader


class F1Receiver:
    _MULTICAST_ANY = "224.0.0.1"
    _SOCKET_TIMEOUT = 10.0
    _BASE_RECV_BYTES = 1400

    def __init__(
        self, output_queue: Queue, thread_end_event: Event, port: int = 20777
    ):
        self._queue = output_queue
        self._port = port
        self._end_event = thread_end_event
        self._socket = None
        self.received_messages = 0

    def connect(self):
        # internet + udp connection opts
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.settimeout(self._SOCKET_TIMEOUT)

        # set socket options
        group = socket.inet_aton(self._MULTICAST_ANY)
        _req = struct.pack("4sL", group, socket.INADDR_ANY)
        self._socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, _req)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind to the server address
        self._socket.bind(("", self._port))

    def listen(self):
        while not self._end_event.is_set():
            try:
                data, address = self._socket.recvfrom(self._BASE_RECV_BYTES)
                packet = PacketHeader.unpack(data)
                if packet:
                    self._queue.put(packet)
                    self.received_messages += 1

            except socket.timeout:
                # check whether the event is set now
                if self._end_event.is_set():
                    print("End event detected. Closing receiver thread.")
                    break
                else:
                    continue

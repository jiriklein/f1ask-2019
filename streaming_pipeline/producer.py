from queue import Queue
from typing import Iterable, Callable
from threading import Event

from streaming_pipeline.structures.packets import PacketCarTelemetryData
from streaming_pipeline.models import Participant
from streaming_pipeline.utils import handle_timeout


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
        while True:
            raw_pkt = handle_timeout(
                self._input_queue,
                self._end_event,
            )
            if self.strategy:
                for _q in self._output_queues:
                    _q.put(self.strategy(raw_pkt))
            else:
                # TODO just write to file
                pass

    @staticmethod
    def strategy_telemetry_packet_participant(
        packet: PacketCarTelemetryData, participant: Participant
    ) -> Participant:
        if isinstance(packet, PacketCarTelemetryData):
            player_car_idx = packet.header.player_car_index
            telemetry_data_player = packet.car_telemetry_data[player_car_idx]
            participant.brake = telemetry_data_player.brake
            participant.speed = telemetry_data_player.speed
            participant.steer = telemetry_data_player.steer
            participant.engine_rpm = telemetry_data_player.engine_rpm
            return participant

    @staticmethod
    def speed_only(
        packet: PacketCarTelemetryData,
    ) -> int:
        if isinstance(packet, PacketCarTelemetryData):
            player_car_idx = packet.header.player_car_index
            telemetry_data_player = packet.car_telemetry_data[player_car_idx]
            print(telemetry_data_player.speed)
            return telemetry_data_player.speed

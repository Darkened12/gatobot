from dataclasses import dataclass
from typing import List


_CHANNELS_TO_WORK_ON: List[List[int]] = [
    [974759972036542484, 3600],  # hoyo, 60min
    [974759995843428422, 14400]  # blue archive, 4h
]


@dataclass
class ChannelsModel:
    id: int
    sleep_time_in_seconds: int


CHANNELS: List[ChannelsModel] = [ChannelsModel(id_, sleep_time) for id_, sleep_time in _CHANNELS_TO_WORK_ON]

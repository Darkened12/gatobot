from dataclasses import dataclass
from typing import List


_CHANNELS_TO_WORK_ON: List[List[int]] = [
    [825282847426347031, 3600],  # hoyo, 60min
    [825282847426347031, 14400]  # blue archive, 4h
]


@dataclass
class ChannelsModel:
    id: int
    sleep_time_in_seconds: int


CHANNELS: List[ChannelsModel] = [ChannelsModel(id_, sleep_time) for id_, sleep_time in _CHANNELS_TO_WORK_ON]

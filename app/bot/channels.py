from dataclasses import dataclass
from typing import List


_CHANNELS_TO_WORK_ON: List[List[int, int]] = [
    [974759972036542484, 1800],  # hoyo
    [974759995843428422, 7200]  # blue archive
]


@dataclass
class ChannelsModel:
    id: int
    sleep_time_in_seconds: int


CHANNELS: List[ChannelsModel] = [ChannelsModel(id_, sleep_time) for id_, sleep_time in zip(_CHANNELS_TO_WORK_ON)]

from dataclasses import dataclass
from typing import List


@dataclass
class EmotionalKeyword:
    keyword: str
    sets: List[str]


TRISTE: EmotionalKeyword = EmotionalKeyword(
    keyword='triste',
    sets=['fudido', 'fudeu', 'despair', 'mal', 'ruim', 'bosta', 'merda', 'morte', 'morra', 'morri', 'sad', 'brasil',
          'overwatch', 'gacha', 'league', 'cf', 'cigarro', 'elon', 'musk', 'paulista', 'carioca', 'anime', 'mangá',
          'hsr', 'wuwa', 'cryo', 'geo']
)

FELIZ: EmotionalKeyword = EmotionalKeyword(
    keyword='feliz',
    sets=['feliz', 'legal', 'bom', 'genshin', 'rata', 'rato', 'cupom', 'pqp', 'brabo', 'pog', 'braba', 'boa', 'salve'
          'nico', 'bonus', 'dinato', 'dartiem', 'denitsu']
)
import discord

from app.models.emotional_keywords_dataset import FELIZ, TRISTE
from app.services.logging_service import logger
from typing import Optional


class CatHappiness:
    def __init__(self):
        self.__happiness: int = 50

    def make_happy(self):
        if self.__happiness == 100:
            return
        self.__happiness += 10

    def make_sad(self):
        if self.__happiness == 0:
            return
        self.__happiness -= 10

    @property
    def happiness(self):
        return 'happy' if self.__happiness >= 50 else 'sad'

    @property
    def happiness_level(self):
        return self.__happiness

    def get_happiness_from_message(self, message: discord.Message) -> Optional[str]:
        for word in message.content.split():
            if word.lower() in FELIZ.sets:
                old_happiness = self.happiness_level
                self.make_happy()
                logger.warn(f'CatHappiness went up - before: "{old_happiness}", now: "{self.happiness_level}", '
                            f'trigger: "{word}".')
                return 'happy'
            if word.lower() in TRISTE.sets:
                old_happiness = self.happiness_level
                self.make_sad()
                logger.warn(f'CatHappiness went down - before: "{old_happiness}", now: "{self.happiness_level}"'
                            f', trigger: "{word}".')
                return 'sad'

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

from sqlalchemy import Column, Integer, String, BigInteger, DateTime

from .base_model import Base


class GifsModel(Base):
    __tablename__ = 'gifs'

    def __repr__(self):
        return f'{self.url}'

    id = Column(Integer, primary_key=True)
    weight = Column(Integer, nullable=False, default=5)
    gif_name = Column(String, default='tenor-gif')
    url = Column(String, nullable=False, unique=True, index=True)
    created_at = Column(DateTime)
    added_by_user_id = Column(BigInteger)


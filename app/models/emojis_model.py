import sqlalchemy
from sqlalchemy import Column, Integer, String, BigInteger, DateTime, URL
from sqlalchemy.orm import relationship
from .base_model import Base
from datetime import datetime
from .emojis_keywords_association_model import EmojisKeywordsAssociation


class EmojisModel(Base):
    __tablename__ = 'emojis'

    def __repr__(self):
        return f'{self.url}'

    id = Column(Integer, primary_key=True)
    keywords = relationship('KeywordsModel', secondary=EmojisKeywordsAssociation, back_populates='keywords')
    emoji_name = Column(String, nullable=False, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.now(), server_default=sqlalchemy.func.current_timestamp(),
                        nullable=False)
    created_by_user_id = Column(BigInteger, default=243332147379830785,
                                server_default=sqlalchemy.text('243332147379830785'), nullable=False)


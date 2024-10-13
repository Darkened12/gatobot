from .base_model import Base
from sqlalchemy import Column, Integer, ForeignKey


class EmojisKeywordsAssociation(Base):
    __tablename__ = 'emojis_keywords_association'

    keyword_id = Column(Integer, ForeignKey('keywords.id', ondelete='CASCADE'), primary_key=True)
    emoji_id = Column(Integer, ForeignKey('emojis.id', ondelete='CASCADE'), primary_key=True)


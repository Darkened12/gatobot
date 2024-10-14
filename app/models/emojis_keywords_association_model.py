from sqlalchemy import Table, Column, Integer, ForeignKey
from .base_model import Base

EmojisKeywordsAssociation = Table(
    'emojis_keywords_association', Base.metadata,
    Column('keyword_id', Integer, ForeignKey('keywords.id', ondelete='CASCADE'), primary_key=True),
    Column('emoji_id', Integer, ForeignKey('emojis.id', ondelete='CASCADE'), primary_key=True)
)

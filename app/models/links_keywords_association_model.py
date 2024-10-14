from sqlalchemy import Table, Column, Integer, ForeignKey
from .base_model import Base

LinksKeywordsAssociation = Table(
    'links_keywords_association', Base.metadata,
    Column('keyword_id', Integer, ForeignKey('keywords.id', ondelete='CASCADE'), primary_key=True),
    Column('link_id', Integer, ForeignKey('links.id', ondelete='CASCADE'), primary_key=True)
)

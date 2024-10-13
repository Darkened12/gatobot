from sqlalchemy import Column, Integer, String, BigInteger, DateTime, URL
from sqlalchemy.orm import relationship
from .base_model import Base
from .links_keywords_association_model import LinksKeywordsAssociation


class LinksModel(Base):
    __tablename__ = 'links'

    def __repr__(self):
        return f'{self.url}'

    id = Column(Integer, primary_key=True)
    weight = Column(Integer, nullable=False, default=5)
    keywords = relationship('KeywordsModel', secondary=LinksKeywordsAssociation, back_populates='keywords')
    link_name = Column(String, default='unknown-link')
    url = Column(String, nullable=False, unique=True, index=True)
    created_at = Column(DateTime)
    added_by_user_id = Column(BigInteger)


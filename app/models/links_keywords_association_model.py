from base_model import Base
from sqlalchemy import Column, Integer, ForeignKey


class LinksKeywordsAssociation(Base):
    __tablename__ = 'links_keywords_association'

    keyword_id = Column(Integer, ForeignKey('keywords.id'), primary_key=True)
    link_id = Column(Integer, ForeignKey('links.id'), primary_key=True)


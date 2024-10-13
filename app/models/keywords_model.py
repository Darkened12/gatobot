from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.orm import relationship

from base_model import Base
from links_keywords_association_model import LinksKeywordsAssociation


class KeywordsModel(Base):
    __tablename__ = 'keywords'

    def __repr__(self):
        return self.keyword

    id = Column(Integer, primary_key=True)
    keyword = Column(VARCHAR(20), nullable=False, unique=True, index=True)
    links = relationship('LinksModel', secondary=LinksKeywordsAssociation, back_populates='links')

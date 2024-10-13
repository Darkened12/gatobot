import sqlalchemy
from sqlalchemy import Column, Integer, VARCHAR, DateTime, BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime

from .base_model import Base
from .links_keywords_association_model import LinksKeywordsAssociation


class KeywordsModel(Base):
    __tablename__ = 'keywords'

    def __repr__(self):
        return self.keyword

    id = Column(Integer, primary_key=True)
    keyword = Column(VARCHAR(20), nullable=False, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.now(), server_default=sqlalchemy.func.current_timestamp(),
                        nullable=False)
    created_by_user_id = Column(BigInteger, default=243332147379830785,
                                server_default=sqlalchemy.text('243332147379830785'), nullable=False)
    links = relationship('LinksModel', secondary=LinksKeywordsAssociation, back_populates='links')

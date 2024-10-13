import sqlalchemy
from sqlalchemy import Column, Integer, String, BigInteger, DateTime, URL
from sqlalchemy.orm import relationship
from .base_model import Base
from datetime import datetime
from .links_keywords_association_model import LinksKeywordsAssociation


class LinksModel(Base):
    __tablename__ = 'links'

    def __repr__(self):
        return f'{self.url}'

    id = Column(Integer, primary_key=True)
    keywords = relationship('KeywordsModel', secondary=LinksKeywordsAssociation, back_populates='keywords')
    link_name = Column(String, default='unknown-link', server_default='unknown-link')
    url = Column(String, nullable=False, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.now(), server_default=sqlalchemy.func.current_timestamp(),
                        nullable=False)
    created_by_user_id = Column(BigInteger, default=243332147379830785,
                                server_default=sqlalchemy.text('243332147379830785'), nullable=False)


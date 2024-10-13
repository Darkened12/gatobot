import discord
import time
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError, OperationalError

from app.models.keywords_model import KeywordsModel
from app.models.links_model import LinksModel
from app.models.links_keywords_association_model import LinksKeywordsAssociation
from app.services.database_service import DatabaseService
from typing import Optional, List


class LinksController:
    def __init__(self, database_service: DatabaseService):
        self.database_service = database_service

    async def is_keyword_in_model(self, keyword: str) -> bool:
        async with self.database_service.session() as session:
            async with session.begin():
                query = (
                    session.query(LinksModel.keywords)
                    .join(LinksModel.keywords)
                    .filter(KeywordsModel.keyword == keyword)
                )
                result = await query.all()
                return len(result) > 0

    # async def add_gif(self, gif: str, user: Optional[discord.User], weight: int = 5):
    #     async with self.database_service.session() as session:
    #         try:
    #             session.add(LinksModel(
    #                 url=gif,
    #                 weight=weight,
    #                 gif_name=f'{datetime.now()}_tenor-gif_{time.time()}.gif',
    #                 created_at=datetime.now(),
    #                 added_by_user_id=user.id if user is not None else None
    #             ))
    #             await session.commit()
    #         except IntegrityError:
    #             await session.rollback()
    #             raise AlreadyExistsError('this gif already exists.')

    async def get_all_links_by_keyword(self, keyword: str) -> List[LinksModel]:
        async with self.database_service.session() as session:
            async with session.begin():
                query = (
                    session.query(LinksModel)
                    .join(LinksModel.keywords)
                    .filter(KeywordsModel.keyword == keyword)
                )
                results = await query.all()
                if not results:
                    raise ValueError(f"No links found for keyword: {keyword}")
                return results

    async def get_random_link_by_keyword(self, keyword: str) -> LinksModel:
        async with self.database_service.session() as session:
            query = (
                session.query(LinksModel)
                .join(LinksModel.keywords)
                .filter(KeywordsModel.keyword == keyword)
                .order_by(func.random())
            )
            result = await query.first()
            if not result:
                raise ValueError(f"No links found for keyword: {keyword}")
            return result


class AlreadyExistsError(Exception):
    pass

import discord
import time
from datetime import datetime

from sqlalchemy import func, insert
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError, OperationalError

from app.controllers.keywords_controller import KeywordsController
from app.models.keywords_model import KeywordsModel
from app.models.links_model import LinksModel
from app.models.links_keywords_association_model import LinksKeywordsAssociation
from app.services.database_service import DatabaseService
from app.services.url_checker_service import is_valid_url
from typing import Optional, List


class LinksController:
    def __init__(self, database_service: DatabaseService):
        self.database_service = database_service
        self.kw_controller = KeywordsController(database_service)

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

    async def add_link(self, url: str, keyword: str = None):
        if is_valid_url(url):
            async with self.database_service.session() as session:
                async with session.begin():
                    new_link = LinksModel(url=url)
                    session.add(new_link)
                    await session.commit()
                    if keyword is not None:
                        keyword_id = await self.kw_controller.get_id_by_keyword(keyword)
                        session.add(LinksKeywordsAssociation(keyword_id=keyword_id, emoji_id=new_link.id))
                        await session.commit()

    async def link_url_to_keyword(self, url: str, keyword: str):
        async with self.database_service.session() as session:
            async with session.begin():
                link_id_result = await session.execute(
                    select(LinksModel.id).filter(LinksModel.url == url)
                )
                link_id = link_id_result.scalars().first()
                keyword_id = await self.kw_controller.get_id_by_keyword(keyword)
                stmt = insert(LinksKeywordsAssociation).values(keyword_id=keyword_id, link_id=link_id)
                await session.execute(stmt)
                await session.commit()


class AlreadyExistsError(Exception):
    pass

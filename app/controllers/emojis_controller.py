from typing import List
from sqlalchemy import func, insert
from sqlalchemy.future import select

from app.models.emojis_keywords_association_model import EmojisKeywordsAssociation
from app.models.emojis_model import EmojisModel
from app.models.keywords_model import KeywordsModel
from app.services.database_service import DatabaseService
from .keywords_controller import KeywordsController


class EmojisController:
    def __init__(self, database_service: DatabaseService):
        self.database_service = database_service
        self.kw_controller = KeywordsController(database_service)

    async def is_keyword_in_model(self, keyword: str) -> bool:
        async with self.database_service.session() as session:
            async with session.begin():
                query = (
                    session.query(EmojisModel.keywords)
                    .join(EmojisModel.keywords)
                    .filter(KeywordsModel.keyword == keyword)
                )
                result = await query.all()
                return len(result) > 0

    async def get_all_links_by_keyword(self, keyword: str) -> List[EmojisModel]:
        async with self.database_service.session() as session:
            async with session.begin():
                query = (
                    session.query(EmojisModel)
                    .join(EmojisModel.keywords)
                    .filter(KeywordsModel.keyword == keyword)
                )
                results = await query.all()
                if not results:
                    raise ValueError(f"No links found for keyword: {keyword}")
                return results

    async def get_random_emoji_by_keyword(self, keyword: str) -> EmojisModel:
        async with self.database_service.session() as session:
            query = (
                session.query(EmojisModel)
                .join(EmojisModel.keywords)
                .filter(KeywordsModel.keyword == keyword)
                .order_by(func.random())
            )
            result = await query.first()
            if not result:
                raise ValueError(f"No links found for keyword: {keyword}")
            return result

    async def add_emoji(self, emoji: str, keyword: str = None):
        async with self.database_service.session() as session:
            async with session.begin():
                new_emoji = EmojisModel(emoji_name=emoji)
                session.add(new_emoji)
                await session.commit()
                if keyword is not None:
                    keyword_id = await self.kw_controller.get_id_by_keyword(keyword)
                    session.add(EmojisKeywordsAssociation(keyword_id=keyword_id, emoji_id=new_emoji.id))
                    await session.commit()

    async def link_emoji_to_keyword(self, emoji: str, keyword: str):
        async with self.database_service.session() as session:
            async with session.begin():
                emoji_id_result = await session.execute(
                    select(EmojisModel.id).filter(EmojisModel.emoji_name == emoji)
                )
                emoji_id = emoji_id_result.scalars().first()
                keyword_id = await self.kw_controller.get_id_by_keyword(keyword)
                stmt = insert(EmojisKeywordsAssociation).values(keyword_id=keyword_id, emoji_id=emoji_id)
                await session.execute(stmt)
                await session.commit()

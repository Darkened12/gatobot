from typing import List
from sqlalchemy import func

from app.models.emojis_model import EmojisModel
from app.models.keywords_model import KeywordsModel
from app.services.database_service import DatabaseService


class EmojisController:
    def __init__(self, database_service: DatabaseService):
        self.database_service = database_service

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
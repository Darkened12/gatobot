from typing import List

from sqlalchemy import func
from sqlalchemy.future import select

from app.models.keywords_model import KeywordsModel
from app.services.database_service import DatabaseService


class KeywordsController:
    def __init__(self, database_service: DatabaseService):
        self.database = database_service

    async def get_id_by_keyword(self, keyword: str) -> int:
        async with self.database.session() as session:
            async with session.begin():
                keyword_result = await session.execute(
                    select(KeywordsModel.id).filter(KeywordsModel.keyword == keyword)
                )
                keyword_record = keyword_result.scalars().first()
                return keyword_record

    async def get_all_keywords(self) -> List[str]:
        async with self.database.session() as session:
            async with session.begin():
                query = session.query(KeywordsModel.keyword)
                return await query.scalars.all()

    async def get_random_keyword(self) -> str:
        async with self.database.session() as session:
            query = session.query(KeywordsModel.keyword).order_by(func.random())
            return await query.scalars.first()

    async def add_keyword(self, keyword: str):
        async with self.database.session() as session:
            async with session.begin():
                new_keyword = KeywordsModel(keyword=keyword)
                session.add(new_keyword)
                await session.commit()
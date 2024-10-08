import discord
import time
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError, OperationalError

from app.models.gifs_model import GifsModel
from app.services.database_service import DatabaseService
from typing import Optional


class GifsController:
    def __init__(self, database_service: DatabaseService):
        self.database_service = database_service

    async def add_gif(self, gif: str, user: Optional[discord.User], weight: int = 5):
        async with self.database_service.session() as session:
            try:
                await session.add(GifsModel(
                    url=gif,
                    weight=weight,
                    gif_name=f'{datetime.now()}_tenor-gif_{time.time()}.gif',
                    created_at=datetime.now(),
                    added_by_user_id=user.id if user is not None else None
                ))
                await session.commit()
            except IntegrityError:
                raise AlreadyExistsError('this gif already exists.')

    async def get_random_gif(self) -> Optional[GifsModel]:
        async with self.database_service.session() as session:
            try:
                stmt = select(GifsModel).order_by(func.random()).limit(1)
                result = await session.execute(stmt)
                gif = result.scalars().first()
                return gif
            except OperationalError:
                return None


class AlreadyExistsError(Exception):
    pass

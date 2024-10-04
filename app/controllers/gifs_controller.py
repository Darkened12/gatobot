import discord
import time
from datetime import datetime

from sqlalchemy import func

from app.models.gifs_model import GifsModel
from app.services.database_service import DatabaseService
from typing import Optional


class GifsController:
    def __init__(self, database_service: DatabaseService):
        self.database_service = database_service

    async def add_gif(self, gif: str, user: Optional[discord.User], weight: int = 5):
        async with self.database_service.session() as session:
            await session.add(GifsModel(
                url=gif,
                weight=weight,
                gif_name=f'{datetime.now()}_tenor-gif_{time.time()}',
                created_at=datetime.now(),
                added_by_user_id=user.id if user is not None else None
            ))
            await session.commit()

    async def get_random_gif(self) -> GifsModel:
        async with self.database_service.session() as session:
            gif = await session.query(GifsModel).order_by(func.random()).first()
            return gif

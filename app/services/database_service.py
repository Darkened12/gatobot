from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


# necessary to import everything so the Base registers.
from app.models.gifs_model import GifsModel
from app.models.base_model import Base


class DatabaseService:
    Base = Base

    def __init__(self, dsn: str, dsn_connector: str, new_database: bool = False):
        self.dsn_connector = dsn_connector
        self.dsn = self.dsn_connector + dsn
        self.new_database = new_database
        self.engine = None
        self.session = None

    def __await__(self):
        return self.init().__await__()

    async def init(self):
        self.engine = await self._get_engine()
        self.session = await self._get_session()
        return self

    async def _get_engine(self):
        engine = create_async_engine(self.dsn, pool_recycle=1200)
        if self.new_database:
            async with engine.begin() as conn:
                await conn.run_sync(self.Base.metadata.drop_all)
                await conn.run_sync(self.Base.metadata.create_all)
        return engine

    async def _get_session(self):
        async_session = sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )
        return async_session

import asyncio
from app.services.database_service import DatabaseService


async def create_database(dsn: str) -> DatabaseService:
    database = DatabaseService(dsn, new_database=True, dsn_connector='sqlite+aiosqlite://')
    return await database.init()


if __name__ == '__main__':
    database_name = input('database name:\\>')
    dsn = f'/{database_name}'
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_database(dsn))

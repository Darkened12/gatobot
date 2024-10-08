import asyncio
import os
from dotenv import load_dotenv
from database_service import DatabaseService

load_dotenv()


async def update_database_schema():
    database = await DatabaseService(
        dsn_connector='sqlite+aiosqlite:///', dsn=os.environ.get('DATABASE'))
    return await database.update_schema()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(update_database_schema())

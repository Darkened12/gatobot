import asyncio
from typing import Coroutine


def run_parallel_task(task: Coroutine):
    loop = asyncio.get_running_loop()
    loop.create_task(task)

import asyncio
import typing
from asyncio import Task, Future
from typing import Optional


if typing.TYPE_CHECKING:
    from app.store import Store


class Poller:
    def __init__(self, store: 'Store'):
        self.store = store
        self.is_running = False
        self.poll_task: Optional[Task] = None

    def _done_callback(self, result: Future):
        if result.exception():
            self.store.app.logger.exception(
                'poller stopped with exception', exc_info=result.exception()
            )
        if self.is_running:
            self.start()

    async def start(self):
        self.poll_task = asyncio.create_task(self.poll())
        self.poll_task.add_done_callback(self._done_callback)
        self.is_running = True

    async def stop(self):
        self.is_running = False
        await self.poll_task

    async def poll(self):
        while self.is_running:
            updates = await self.store.vk_api.poll()
            await self.store.bots_manager.handle_updates(updates)

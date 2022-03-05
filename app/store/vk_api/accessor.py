import uuid
import typing
from typing import Optional

import aiohttp
from aiohttp.client import ClientSession

from app.base.base_accessor import BaseAccessor
from app.store.vk_api.dataclasses import Message, Update, UpdateObject, UpdateMessage
from app.store.vk_api.poller import Poller

if typing.TYPE_CHECKING:
    from app.web.app import Application


class VkApiAccessor(BaseAccessor):
    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.session: Optional[ClientSession] = None
        self.key: Optional[str] = None
        self.server: Optional[str] = None
        self.poller: Optional[Poller] = None
        self.ts: Optional[int] = None

    async def connect(self, app: "Application"):
        self.poller = Poller(self.app.store)
        self.session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False))
        try:
            await self._get_long_poll_service()
        except Exception as e:
            self.logger.error('Exception', exc_info=e)
        self.logger.info('start polling')
        await self.poller.start()

    async def disconnect(self, app: "Application"):
        if self.poller:
            await self.poller.stop()
        if self.session:
            await self.session.close()

    @staticmethod
    def _build_query(host: str, method: str, params: dict) -> str:
        url = host + method + "?"
        if "v" not in params:
            params["v"] = "5.131"
        url += "&".join([f"{k}={v}" for k, v in params.items()])
        return url

    async def _get_long_poll_service(self):
        params = {
            'access_token': self.app.config.bot.token,
            'group_id': self.app.config.bot.group_id
        }
        url = self._build_query('https://api.vk.com/method/', 'groups.getLongPollServer', params=params)
        async with self.session.get(url) as resp:
            data = await resp.json()
            self.key, self.server, self.ts = data['response']['key'], data['response']['server'], data['response']['ts']

    async def poll(self):
        updates = []
        url = self._build_query(
            host=self.server,
            method='',
            params={
                'act': 'a_check',
                'key': self.key,
                'ts': self.ts,
                'wait': 25
            }
        )
        async with self.session.get(url) as resp:
            data = await resp.json()
            self.logger.info(data)
            self.ts = data['ts']
            raw_updates = data['updates']
            for raw_update in raw_updates:
                update_type, message = raw_update['type'], raw_update['object']['message']
                update = Update(
                    type=update_type,
                    object=UpdateObject(
                        message=UpdateMessage(
                            from_id=message['from_id'],
                            text=message['text'],
                            id=message['id']
                        )
                    )
                )
                updates.append(update)
        return updates

    async def send_message(self, message: Message) -> None:
        params = {
            'access_token': self.app.config.bot.token,
            'user_id': message.user_id,
            'message': message.text,
            'random_id': uuid.uuid4().int,
            'peer_id': '-' + str(self.app.config.bot.group_id)
        }
        url = self._build_query('https://api.vk.com/method/', 'messages.send', params=params)

        async with self.session.post(url) as resp:
            data = await resp.json()
            self.logger.info(data)

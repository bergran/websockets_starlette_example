# -*- coding: utf-8 -*-
import json
import logging

from starlette.websockets import WebSocket

import constants
from core.handlers.websocket import WebSocketEndpointCustom


ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger = logging.getLogger('ws')
logger.propagate = False
logger.addHandler(ch)


class WebsocketView(WebSocketEndpointCustom):

    def get_params(self, websocket: WebSocket) -> dict:
        params_raw = websocket.get('query_string', b'').decode('utf-8')
        return {param.split('=')[0]: param.split('=')[1] for param in params_raw.split('&')}

    async def on_connect(self, websocket: WebSocket):
        self.channel_name = self.get_params(websocket).get('username', 'default_name')
        if self.channel_name == constants.__ALL__:
            await websocket.close()

        await websocket.accept()
        await self.login_user(websocket, self.channel_name)

    async def on_disconnect(self, websocket: WebSocket, close_code: int):
        await self.unlogin_user(websocket, self.channel_name)
        await super().on_disconnect(websocket, close_code)

    async def on_receive(self, ws, data):
        await self.send_message(self.get_channel_name(constants.__ALL__), 'receive_message', data, self.channel_name)

    async def login_user(self, websocket, name):
        app = self.scope.get('app', None)
        users = await self.get_users()
        users.append(name)
        logger.info('login_user: {}'.format(name))
        await app.redis_cache.set('users', json.dumps(users))
        await self.send_message(
            self.get_channel_name(constants.__ALL__),
            'connected_user',
            json.dumps({'message': 'user connected', 'users': users}),
            self.channel_name
        )

    async def unlogin_user(self, websocket, name):
        app = self.scope.get('app', None)
        users = await self.get_users()
        logger.info('unlogin_user: Logout user to ws: {}'.format(name))
        await app.redis_cache.set('users', json.dumps(list(filter(lambda x: x != name, users))))
        await self.send_message(self.get_channel_name(constants.__ALL__), 'disconnected_user', '{}', self.channel_name)

    async def send_message(self, channel, type, message_raw, username):
        message = json.loads(message_raw)
        message.update({'user': username, 'type': type})
        logger.info('send_message: User {} send: {}'.format(username, message_raw))
        await self.pub.publish_json(channel, message)

    async def get_users(self):
        app = self.scope.get('app', None)
        return json.loads(await app.redis_cache.get('users') or '[]')
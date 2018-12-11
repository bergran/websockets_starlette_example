# -*- coding: utf-8 -*-
import asyncio
import json
import logging

import aioredis
from aioredis.pubsub import Receiver
from starlette import status
from starlette.endpoints import WebSocketEndpoint
from starlette.websockets import WebSocket, WebSocketState

import constants


logger = logging.getLogger('websocket')


class WebSocketEndpointCustom(WebSocketEndpoint):
    channel_name = None

    def get_channel_name(self, name):
        return 'channel:{}'.format(name)

    async def __call__(self, receive, send):
        redis_host = 'redis://{}'.format(self.scope.get('app').settings.REDIS_HOST)
        self.pub = await aioredis.create_redis(redis_host)
        self.sub = await aioredis.create_redis(redis_host)
        websocket = WebSocket(self.scope, receive=receive, send=send)
        await self.on_connect(websocket)
        await asyncio.gather(
            self.listen_ws(websocket),
            self.listen_redis(
                websocket,
                [self.get_channel_name(constants.__ALL__), self.get_channel_name(self.channel_name)])
        )

    async def listen_redis(self, websocket, channels):
        channel = channels.pop(0)
        try:
            mpsc = Receiver(loop=asyncio.get_event_loop())
            await self.sub.subscribe(
                mpsc.channel(channel),
                *(mpsc.channel(channel) for channel in channels)
            )
            async for channel, msg in mpsc.iter():
                if websocket.client_state == WebSocketState.CONNECTED:
                    await websocket.send_bytes(msg)
        except:
            import traceback
            traceback.print_exc()
            await self.close_connections()
        finally:
            logger.info('Connection closed')

    async def listen_ws(self, websocket):
        close_code = status.WS_1000_NORMAL_CLOSURE

        try:
            while True:
                message = await websocket.receive()
                if message["type"] == "websocket.receive":
                    data = await self.decode(websocket, message)
                    await self.on_receive(websocket, data)
                elif message["type"] == "websocket.disconnect":
                    close_code = int(message.get("code", status.WS_1000_NORMAL_CLOSURE))
                    break
        except Exception as exc:
            close_code = status.WS_1011_INTERNAL_ERROR
            raise exc from None
        finally:
            await self.on_disconnect(websocket, close_code)

    async def on_disconnect(self, websocket: WebSocket, close_code: int):
        await super().on_disconnect(websocket, close_code)
        await self.close_connections()

    async def close_connections(self):
        await self.sub.unsubscribe(
            self.get_channel_name(constants.__ALL__),
            *[self.get_channel_name(self.channel_name)])
        self.pub.close()
        self.sub.close()

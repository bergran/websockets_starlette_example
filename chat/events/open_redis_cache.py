# -*- coding: utf-8 -*-
import asyncio

import aioredis


def open_redis_cache(app):
    async def wrapper():
        try:
            app.redis_cache = await aioredis.create_redis('redis://{}'.format(app.settings.REDIS_HOST))
        except:
            asyncio.get_event_loop().stop()
            asyncio.get_event_loop().close()
    return wrapper

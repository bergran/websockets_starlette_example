# -*- coding: utf-8 -*-

import asyncio
import aioredis


async def reader(channel):
    while await channel.wait_message():
        msg = await channel.get_json()
        print("Got Message:", msg)


async def main():
    pub = await aioredis.create_redis(
        'redis://localhost')

    for i in range(5):
        await asyncio.sleep(3)
        res = await pub.publish_json('channel:__ALL__', {'hello': 'world'})
        print(res)
        # assert res == 1


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())

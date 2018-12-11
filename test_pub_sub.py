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
    sub = await aioredis.create_redis(
        'redis://localhost')
    res = await sub.subscribe(*['chan:1', 'chan:2'])
    ch1 = res[0]

    tsk = asyncio.ensure_future(reader(ch1))

    await pub.publish_json('chan:1', ["Hello", "world"])

    await sub.unsubscribe('chan:1')
    await tsk
    sub.close()
    pub.close()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())

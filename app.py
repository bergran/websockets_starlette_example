import os

import uvicorn

from chat.events.open_redis_cache import open_redis_cache
from chat.urls import setup_urls
from core.handlers.app import StarletteCustom


app = StarletteCustom(template_directory='templates')
app.add_event_handler('startup', open_redis_cache(app))
setup_urls(app)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, loop='asyncio', proxy_headers=True)

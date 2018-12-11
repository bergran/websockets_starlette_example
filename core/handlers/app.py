# -*- coding: utf-8 -*-
from starlette.applications import Starlette
from project import settings


class StarletteCustom(Starlette):
    redis_cache = None

    def __init__(self, *args, **kwargs):
        super(StarletteCustom, self).__init__(*args, **kwargs)
        self.settings = settings

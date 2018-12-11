# -*- coding: utf-8 -*-

from starlette.endpoints import HTTPEndpoint
from starlette.responses import HTMLResponse


class HomeView(HTTPEndpoint):
    async def get(self, request):
        template = self.scope.get('app').get_template('index.html')
        content = template.render()
        return HTMLResponse(content)

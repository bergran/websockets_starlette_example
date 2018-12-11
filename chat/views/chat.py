# -*- coding: utf-8 -*-
from starlette.endpoints import HTTPEndpoint
from starlette.responses import Response, HTMLResponse

from core.handlers.templates import env


class ChatView(HTTPEndpoint):
    async def get(self, request):
        user = request.query_params.get('user')
        if not user:
            return Response(status_code=404)
        template = env.get_template('chat.html')
        host = request.url_for('ws')
        content = template.render(url='{}?username={}'.format(host, user), user=user)
        return HTMLResponse(content)

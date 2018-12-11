# -*- coding: utf-8 -*-

from chat.views.chat import ChatView
from chat.views.home import HomeView
from chat.views.websocket import WebsocketView


def setup_urls(app):
    app.add_route('/', HomeView, name='home')
    app.add_route('/chat', ChatView, name='chat')
    app.add_websocket_route('/ws', WebsocketView, name='ws')

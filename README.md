# Websocket chat starlette with Channel Layer

This proyect it's a example to the community because [starlette](https://www.starlette.io/) is a new async framework and
it has few examples of how to build the app and in this case how to build websockets with channel layer.

# Dependencies

* Docker
* docker-compose
* Python >= 3.6

# How to build example?

* Create in the project root a file with `REDIS_HOST` where you put route to redis without `redis://`
* execute `docker-compose up -d`, this will execute app

# Routes

* `/` Home view. It's a little form where you put your username.
* `/chat` ChatView. It's chat view where will connect to the Websocket view and list all messages incoming from all users.
* `/ws` WebsocketView. It's the interface where clients will connect to the chat.

# Author

Ángel Berhó(Bergran)

# Contributors

None

# How to contribute?

Please, make a fork from `develop` branch and create your changes. You should remember to update your branch
before make pull request.

I will check pull request 1-2 once times to week. Thank you.
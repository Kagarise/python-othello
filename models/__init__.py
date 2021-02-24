from models.socket import socketIO


def init_app(app):
    socketIO.init_app(app)
    return app

from routes.api import api


def init_app(app):
    app.register_blueprint(api)

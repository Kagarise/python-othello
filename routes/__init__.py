from routes.api import api
from routes.statistics import api_statistics


def init_app(app):
    app.register_blueprint(api)
    app.register_blueprint(api_statistics)

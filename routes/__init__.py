from routes.action import action


def init_app(app):
    app.register_blueprint(action)

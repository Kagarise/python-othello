from flask import Flask
from flask_cors import CORS

import models
import routes
from config.secret_config import SOCKET_KEY


def create_app():
    app = Flask(__name__)
    # SocketIO 密匙
    app.config['SECRET_KEY'] = SOCKET_KEY
    # 路由跨域
    CORS(app, supports_credentials=True)
    routes.init_app(app)
    models.init_app(app)
    return app

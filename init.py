import logging

from flask import Flask
from flask_cors import CORS

import db
import models
import routes


# from config.secret_config import SOCKET_KEY


def create_app():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    app = Flask(__name__)
    # SocketIO 密匙
    # app.config['SECRET_KEY'] = SOCKET_KEY
    # 路由跨域
    CORS(app, supports_credentials=True)
    db.init_app(app)
    routes.init_app(app)
    models.init_app(app)
    return app

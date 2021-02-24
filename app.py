from init import create_app
from config.app_config import SERVER_INFO
from models import socketIO

if __name__ == "__main__":
    app = create_app()
    socketIO.run(app, **SERVER_INFO)

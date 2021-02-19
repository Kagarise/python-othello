import numpy as np
from flask import Flask, request, Blueprint
from flask_cors import CORS

from config.app_config import SERVER_INFO
from utils.result import Result
from config.othello_config import OthelloConfig as Config
from config.othello_config import PlayerType
from models.players import *

api = Blueprint('api', __name__, url_prefix='/api')


def get_player(player):
    if player == PlayerType.GREEDY_NUMBER:
        return GreedyNumberPlayer()
    elif player == PlayerType.RANDOM:
        return RandomPlayer()
    elif player == PlayerType.GREEDY_SCORE:
        return GreedyScorePlayer()
    elif player == PlayerType.ALPHA_BETA:
        return AlphaBetaPlayer()
    elif player == PlayerType.UCT:
        return UCTPlayer()
    elif player == PlayerType.DEEP_LEARNING:
        return DeepLearningPlayer()


@api.route("/action", methods=['post'])
def get_action():
    board = np.array(request.json.get('board'), dtype=np.int8)
    color = request.json.get('color')
    player_type = request.json.get('player')
    # 参数缺失
    if board is None or color is None or player_type is None:
        return Result.error(400, 'Args error!')
    # board参数错误
    if board.shape != (Config.SIZE, Config.SIZE):
        return Result.error(403, 'Board error!')
    # color参数错误
    if color != Config.BLACK and color != Config.WHITE:
        return Result.error(403, 'Color error!')
    # player参数错误
    player = get_player(player_type)
    if player is None:
        return Result.error(403, 'Player error!')
    x, y = player.get_action(board, color)
    # 无法得到解
    if x is None or y is None:
        return Result.error(406, 'Move error!')
    else:
        return Result.success({'x': x, 'y': y})


if __name__ == "__main__":
    app = Flask(__name__)
    # 全局跨域
    CORS(app, supports_credentials=True)
    # 公共前缀api
    app.register_blueprint(api)
    app.run(**SERVER_INFO)

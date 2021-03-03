import logging

import numpy as np
from flask import request, Blueprint

from config.room_config import RoomConfig
from models.redis import r_list_exists, r_list_create
from utils.id import create_room_id
from utils.ip import get_ip

from utils.result import Result
from config.othello_config import OthelloConfig as Config
from config.othello_config import PlayerType
from models.players import *

api = Blueprint('api', __name__, url_prefix='/api')


def get_player(player):
    if player == PlayerType.RANDOM:
        return RandomPlayer()
    elif player == PlayerType.GREEDY_NUMBER:
        return GreedyNumberPlayer()
    elif player == PlayerType.GREEDY_SCORE:
        return GreedyScorePlayer()
    elif player == PlayerType.UCT:
        return UCTPlayer()
    elif player == PlayerType.ALPHA_BETA:
        return AlphaBetaPlayer()
    elif player == PlayerType.DEEP_LEARNING:
        return DeepLearningPlayer()


@api.route("/action", methods=['post'])
def action():
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


# @return: room_id
@api.route("/create_room", methods=['post'])
def create_room():
    room_id = create_room_id(RoomConfig.OTHELLO_ROOM_ID_LENGTH)
    room_name = RoomConfig.OTHELLO_ROOM + room_id
    while r_list_exists(room_name) is False:
        room_id = create_room_id(RoomConfig.OTHELLO_ROOM_ID_LENGTH)
        room_name = RoomConfig.OTHELLO_ROOM + room_id
    # 创建房间
    r_list_create(room_name, RoomConfig.OTHELLO_ROOM_SIZE)
    logging.info(get_ip() + ' 创建了 ' + room_name)
    return Result.success({'room_id': room_id})

# @action.route("/init/redis", methods=['post'])
# def init_redis():
#     from models.redis import redis_client
#     user_list = request.json.get('user_list')
#     init_length = request.json.get('init_length')
#     if user_list is None or init_length is None:
#         return Result.error(400, 'Args error!')
#     pipe = redis_client.pipeline()
#     for idx in range(init_length):
#         idx += 1
#         for value in user_list:
#             pipe.rpush(idx, value)
#     pipe.execute()
#     return Result.success()
#
#
# @action.route("/delete/redis", methods=['post'])
# def delete_redis():
#     from models.redis import redis_client
#     # user_list = request.json.get('user_list')
#     init_length = request.json.get('init_length')
#     if init_length is None:
#         return Result.error(400, 'Args error!')
#     pipe = redis_client.pipeline()
#     for idx in range(init_length):
#         idx += 1
#         for j in range(2):
#             pipe.rpop(idx)
#     pipe.execute()
#     return Result.success()

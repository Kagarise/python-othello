from flask import Blueprint, request

from config.othello_config import PlayerType
from db import db_session
from db.statistics import Statistics
from utils.result import Result

api_statistics = Blueprint('api_statistics', __name__, url_prefix='/api/statistics')


@api_statistics.route("/add", methods=['post'])
def add():
    player_type = request.json.get('player_type')
    is_win = request.json.get('is_win')
    is_draw = request.json.get('is_draw')
    if player_type is None or (is_win is None and is_draw is None):
        return Result.error(400, 'Args error!')
    if player_type not in PlayerType._value2member_map_:
        return Result.error(400, 'Unknown Player Type')
    if is_draw is None:
        is_draw = False
    statistics = Statistics.query.filter(Statistics.player_type == player_type).first()
    if statistics is None:
        statistics = Statistics(player_type)
        db_session.add(statistics)
    statistics.total += 1
    if is_draw:
        statistics.draw += 1
    elif is_win:
        statistics.win += 1
    db_session.commit()
    return Result.success()


@api_statistics.route("/get", methods=['get'])
def get():
    player_type = request.json.get('player_type')
    if player_type is None:
        return Result.error(400, 'Args error!')
    if player_type not in PlayerType._value2member_map_:
        return Result.error(400, 'Unknown Player Type')
    statistics = Statistics.query.filter(Statistics.player_type == player_type).first()
    if statistics is None:
        statistics = Statistics(player_type)
    return Result.success(statistics.serialize())

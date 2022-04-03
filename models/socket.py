import logging

from flask_socketio import SocketIO, emit, join_room, leave_room, rooms

from config.room_config import RoomConfig
from models.pedis import r_list_exists, r_list_create, r_list_set, r_list_get_all, r_list_clear
from utils.id import create_room_id
from utils.ip import get_ip

# 开启跨域
socketIO = SocketIO(cors_allowed_origins='*')


# 建立连接
# @return: user_id
@socketIO.event
def connect():
    ip = get_ip()
    emit('response_connect', {'code': 200, 'msg': ip + '连接成功', 'user_id': ip})
    logging.debug(ip + " 连接成功")


# 关闭连接
@socketIO.event
def disconnect():
    user_id = get_ip()
    if len(rooms()) > 1:
        room_name = rooms()[1]
        user_list = r_list_get_all(room_name)
        for i in range(len(user_list)):
            if user_list[i] == user_id:
                user_list[i] = ''
                r_list_set(room_name, i, '')
                emit('response_leave', {'code': 200, 'msg': user_id + '离开了' + room_name, 'user_list': user_list},
                     room=room_name)
                leave_room(room_name)
                break
        logging.debug(user_id + ' 离开了 ' + room_name)
        is_empty = True
        for val in user_list:
            if val != '':
                is_empty = False
                break
        if is_empty:
            r_list_clear(room_name)
            logging.info(user_id + ' 关闭了 ' + room_name)
    logging.debug(user_id + " 断开连接")


# 创建房间
# @params: user_id
# @return: room_id
@socketIO.event
def create(data):
    user_id = data['user_id']
    # 随机生成房间号
    room_id = create_room_id(RoomConfig.OTHELLO_ROOM_ID_LENGTH)
    room_name = RoomConfig.OTHELLO_ROOM + room_id
    while r_list_exists(room_name) is False:
        room_id = create_room_id(RoomConfig.OTHELLO_ROOM_ID_LENGTH)
        room_name = RoomConfig.OTHELLO_ROOM + room_id
    # 创建房间
    r_list_create(room_name, RoomConfig.OTHELLO_ROOM_SIZE)
    emit('response_create', {'code': 200, 'msg': user_id + '创建了' + room_name, 'room_id': room_id})
    logging.error("socketIO创建房间")


# 加入房间
# @params: user_id, room_id
# @return: user_list
@socketIO.event
def join(data):
    user_id = data['user_id']
    room_name = RoomConfig.OTHELLO_ROOM + data['room_id']
    user_list = r_list_get_all(room_name)
    if not user_list:
        emit('response_join', {'code': 405, 'msg': '房间不存在'})
    elif user_id in user_list:
        emit('response_join', {'code': 403, 'msg': '已经在房间中，不可重复加入'})
    elif '' not in user_list:
        emit('response_join', {'code': 416, 'msg': '房间已满员'})
    else:
        for i in range(len(user_list)):
            if user_list[i] == '':
                user_list[i] = user_id
                r_list_set(room_name, i, user_id)
                join_room(room_name)
                emit('response_join', {'code': 200, 'msg': user_id + '加入了' + room_name, 'user_list': user_list},
                     room=room_name)
                logging.debug(user_id + ' 加入了 ' + room_name)
                break


# 离开房间
# @params: user_id, room_id
# @return: user_list
@socketIO.event
def leave(data):
    user_id = data['user_id']
    room_name = RoomConfig.OTHELLO_ROOM + data['room_id']
    user_list = r_list_get_all(room_name)
    if user_id not in user_list:
        emit('response_leave', {'code': 400, 'msg': '离开错误，不在房间中'})
    else:
        for i in range(len(user_list)):
            if user_list[i] == user_id:
                user_list[i] = ''
                r_list_set(room_name, i, '')
                leave_room(room_name)
                emit('response_leave', {'code': 200, 'msg': user_id + '离开了' + room_name, 'user_list': user_list},
                     room=room_name)
                logging.debug(user_id + ' 离开了 ' + room_name)
                break
        is_empty = True
        for val in user_list:
            if val != '':
                is_empty = False
                break
        if is_empty:
            r_list_clear(room_name)
            logging.info(user_id + ' 关闭了 ' + room_name)


# 开始游戏
# @params: room_id
@socketIO.event
def start_game(data):
    room_name = RoomConfig.OTHELLO_ROOM + data['room_id']
    emit('response_start_game', room=room_name)


# 行动
# @params: data
# @return: data
@socketIO.event
def action(data):
    room_name = RoomConfig.OTHELLO_ROOM + data['room_id']
    emit('response_action', data, room=room_name)

# 进入房间
# @params: room_id, user_id
# @return: user_id, user_list
# @socketIO.event
# def join(data):
#     room_id = data['room_id']
#     user_id = data['user_id']
#     # 判断是创建房间还是加入房间
#     user_list = r_set_get(room_id)
#     logging.debug({"user_list": user_list})
#     if r_set_count(room_id, user_id):
#         emit('response_join', {'code': 403, 'msg': '已经在房间中，不可重复加入'})
#     elif len(user_list) >= 2:
#         emit('response_join', {'code': 416, 'msg': '房间已满员'})
#     else:
#         r_set_add(room_id, user_id)
#         user_list = r_set_get(room_id)
#         logging.debug({"new_user_list": user_list})
#         join_room(room_id)
#         emit('response_join',
#              {'code': 200, 'msg': user_id + '进入房间' + room_id, 'user_id': user_id, "user_list": user_list},
#              room=room_id)
#         logging.debug(user_id + '进入房间' + room_id)


# 离开房间
# @params: room_id, user_id
# @return: user_id, user_list
# @socketIO.event
# def leave(data):
#     room_id = data['room_id']
#     user_id = data['user_id']
#     r_set_remove(room_id, user_id)
#     leave_room(room_id)
#     emit('response_leave',
#          {'code': 200, 'msg': user_id + '离开房间' + room_id, 'user_id': user_id,
#           "user_list": r_set_get(room_id)}, room=room_id)
#     logging.debug(user_id + "离开房间" + room_id)


# 关闭房间
# @params: room_id user_id
# @socketIO.event()
# def close_room(data):
#     room_id = data['room_id']
#     user_id = data['user_id']
#     r_set_remove(room_id)
#     close_room(room_id)
#     emit('response_close_room', {'code': 200, 'msg': user_id + '关闭了房间' + room_id}, room=room_id)
#     logging.debug(user_id + '关闭了房间' + room_id)


# 房间信息
# @socketIO.event
# def my_room_event(data):
#     room = data['room']
#     user_list = r_set_get(room)
#     emit('response_room_info', {'code': 200, 'msg': "获取房间信息成功", 'user_list': user_list})
#     logging.debug(get_ip() + " room info: " + str(rooms()[1]))

from flask_socketio import SocketIO, emit, join_room, rooms, leave_room, close_room

from utils.ip import get_ip

# 开启跨域
socketIO = SocketIO(cors_allowed_origins='*', async_mode='eventlet')


# 建立连接
@socketIO.event
def connect():
    ip = get_ip()
    emit('response_connect', {'msg': 'connect successful!', 'info': ip})
    print(ip + " connect successful!")


# 关闭连接
@socketIO.event
def disconnect():
    ip = get_ip()
    print(ip + " disconnect successful!")


# 进入房间
@socketIO.event
def join(data):
    join_room(data['room'])
    emit('response_join', {'msg': 'In room: ' + ', ' + str(rooms()[1]), 'info': data['info']}, room=data['room'])
    print(str(data['info']) + " join room: " + str(rooms()[1]))


# 离开房间
@socketIO.event
def leave(data):
    leave_room(data['room'])
    emit('response_leave', {'msg': 'Leave rooms: ' + ', ' + str(rooms()[1]), 'info': data['info']}, room=data['room'])
    print(str(data['info']) + " leave room: " + str(rooms()[1]))


# 关闭房间
@socketIO.on('close_room')
def on_close_room(data):
    emit('response_close_room', {'msg': 'Room ' + data['room'] + ' is closing!'}, to=data['room'])
    print(get_ip() + " close room: " + str(rooms()[1]))
    close_room(data['room'])


# 房间信息
@socketIO.event
def my_room_event(message):
    emit('response_room_info', {'data': message['data']}, to=message['room'])
    print(get_ip() + " room info: " + str(rooms()[1]))

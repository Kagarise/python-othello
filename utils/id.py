import random


def create_room_id(length):
    option = '01234567890abcdefghijklmnopqrstuvwxyz'
    room_id = ''
    for idx in range(length):
        room_id += random.choice(option)
    return room_id

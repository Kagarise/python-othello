import json
import numpy

from models.players import UCTPlayer

DIR = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))  # 方向向量


# 放置棋子，计算新局面
def place(board, x, y, color):
    if x < 0:
        return False
    board[x][y] = color
    valid = False
    for d in range(8):
        i = x + DIR[d][0]
        j = y + DIR[d][1]
        while 0 <= i and i < 8 and 0 <= j and j < 8 and board[i][j] == -color:
            i += DIR[d][0]
            j += DIR[d][1]
        if 0 <= i and i < 8 and 0 <= j and j < 8 and board[i][j] == color:
            while True:
                i -= DIR[d][0]
                j -= DIR[d][1]
                if i == x and j == y:
                    break
                valid = True
                board[i][j] = color
    return valid


# 处理输入，还原棋盘
def initBoard():
    fullInput = json.loads(input())
    requests = fullInput["requests"]
    responses = fullInput["responses"]
    board = numpy.zeros((8, 8), dtype=numpy.int)
    board[3][4] = board[4][3] = 1
    board[3][3] = board[4][4] = -1
    myColor = 1
    if requests[0]["x"] >= 0:
        myColor = -1
        place(board, requests[0]["x"], requests[0]["y"], -myColor)
    turn = len(responses)
    for i in range(turn):
        place(board, responses[i]["x"], responses[i]["y"], myColor)
        place(board, requests[i + 1]["x"], requests[i + 1]["y"], -myColor)
    return board, myColor


def botZone():
    board, color = initBoard()
    x, y = UCTPlayer().get_action(board, color)
    print(json.dumps({"response": {"x": x, "y": y}}))

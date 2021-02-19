import numpy as np

from config.othello_config import OthelloConfig as Config


class Game(object):
    def __init__(self, board=None):
        if board is None:
            board = np.zeros((Config.SIZE, Config.SIZE), dtype=np.int8)
            board[3, 4] = board[4, 3] = Config.BLACK  # |白|黑|
            board[3, 3] = board[4, 4] = Config.WHITE  # |黑|白|
        self.board = board

    def display(self):
        index = '01234567'
        print(' ', *index[:Config.SIZE])
        for c, r in zip(index, self.board):
            print(c, *map('-WB'.__getitem__, r))

    def place(self, x=-1, y=-1, color=Config.EMPTY, check_only=False):
        if x < 0 or y < 0 or x >= 8 or y >= 8 or self.board[x][y] != Config.EMPTY:
            return False
        if not check_only:
            self.board[x, y] = color
        valid = False
        for d in range(len(Config.DIR)):
            i = x + Config.DIR[d][0]
            j = y + Config.DIR[d][1]
            while 0 <= i < 8 and 0 <= j < 8 and self.board[i, j] == -color:
                i += Config.DIR[d][0]
                j += Config.DIR[d][1]
            if 0 <= i < 8 and 0 <= j < 8 and self.board[i, j] == color:
                while True:
                    i -= Config.DIR[d][0]
                    j -= Config.DIR[d][1]
                    if i == x and j == y:
                        break
                    if check_only:
                        return True
                    valid = True
                    self.board[i, j] = color
        return valid

    def get_valid_moves(self, color, get_next_state=False):
        moves = []
        states = []
        for i in range(Config.SIZE):
            for j in range(Config.SIZE):
                if self.board[i, j] == Config.EMPTY:
                    if get_next_state:
                        game = Game(self.board.copy())
                        if game.place(i, j, color):
                            moves.append((i, j))
                            states.append(game.board)
                    elif self.place(i, j, color, True):
                        moves.append((i, j))
        if get_next_state:
            return moves, states
        return moves

    def get_number(self, color=None):
        if color is None:
            b = w = 0
            for i in range(Config.SIZE):
                for j in range(Config.SIZE):
                    if self.board[i, j] == Config.BLACK:
                        b += 1
                    elif self.board[i, j] == Config.WHITE:
                        w += 1
            return b, w
        else:
            num = 0
            for i in range(Config.SIZE):
                for j in range(Config.SIZE):
                    if self.board[i, j] == color:
                        num += 1
            return num

    # def get_score(self, color=None):
    #     if color is None:
    #         b = w = 0
    #         for i in range(Config.SIZE):
    #             for j in range(Config.SIZE):
    #                 if self.board[i, j] == Config.BLACK:
    #                     b += Config.WEIGHTS[i, j]
    #                 elif self.board[i, j] == Config.WHITE:
    #                     w += Config.WEIGHTS[i, j]
    #         return b, w
    #     else:
    #         score = 0
    #         for i in range(Config.SIZE):
    #             for j in range(Config.SIZE):
    #                 if self.board[i, j] == color:
    #                     score += Config.WEIGHTS[i, j]
    #         return score

    def get_score(self, color):
        return sum(sum(self.board * Config.WEIGHTS)) * color

    def is_finish(self):
        return self.get_valid_moves(Config.BLACK) == [] and self.get_valid_moves(Config.WHITE) == []

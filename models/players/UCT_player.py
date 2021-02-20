import random
import time
from math import sqrt, log

from models.player import Player
from config.othello_config import OthelloConfig as Config


class UCTPlayer(Player):
    def get_action(self, board, color):
        state = State(board, color)
        moves = state.get_valid_moves()
        if len(moves) == 0:
            return -1, -1
        uct = UCT()
        x, y = uct.uct_search(state)
        # print(x, y)
        return x, y


class UCT(object):
    def uct_search(self, state):
        self.N = 0
        root = Node(state)
        start_time = time.time()
        while time.time() - start_time < Config.UCT_MAX_TIME:
        # time = 0
        # while time < 5:
        #     time += 1
            child = self.tree_policy(root)
            value = self.default_policy(child)
            self.N += 1
            self.backup(child, value)
        return self.best_child(root, Config.UCB_USE)[0]

    def tree_policy(self, node):
        if not node.is_expand:
            self.expand(node)
        return self.best_child(node, Config.UCB_EXPLORE)[1]

    def expand(self, node):
        node.is_expand = True
        moves = node.state.get_valid_moves()
        for move in moves:
            child_state = State(node.state.board.copy(), node.state.color)
            child_state.play(move[0], move[1])
            node.children[move] = Node(child_state, node)

    def best_child(self, node, c):
        return max(node.children.items(), key=lambda item: item[1].cal_ucb(self.N, c))

    def default_policy(self, node):
        state = State(node.state.board.copy(), node.state.color)
        while not state.is_finish():
            state.random_play()
        return state.get_value(-node.state.color)

    def backup(self, parent, value):
        while parent is not None:
            parent.total += 1
            parent.value += value
            parent = parent.parent


class Node(object):
    def __init__(self, state, parent=None):
        self.state = state
        self.total = 0
        self.value = 0.0
        self.parent = parent
        self.children = {}
        self.is_expand = False

    def cal_ucb(self, N, c):
        if self.total == 0:
            return Config.INF
        return self.value / self.total + c * sqrt(log(N) / self.total)


class State(object):
    def __init__(self, board, color):
        self.board = board
        self.color = color

    def play(self, x, y):
        self.place(x, y)
        self.color = - self.color

    def place(self, x=-1, y=-1, color=None, check_only=False):
        if color is None:
            color = self.color
        if x < 0 or y < 0 or x >= 8 or y >= 8 or self.board[x, y] != Config.EMPTY:
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

    def get_valid_moves(self, color=None, get_next_state=False):
        if color is None:
            color = self.color
        moves = []
        states = []
        for i in range(Config.SIZE):
            for j in range(Config.SIZE):
                if self.board[i, j] == Config.EMPTY:
                    if get_next_state:
                        state = State(self.board.copy(), color)
                        if state.place(i, j):
                            moves.append((i, j))
                            states.append(state.board)
                    elif self.place(i, j, color, True):
                        moves.append((i, j))
        if get_next_state:
            return moves, states
        return moves

    def random_play(self):
        moves = self.get_valid_moves()
        if len(moves) == 0:
            self.play(-1, -1)
            return
        x, y = random.choice(moves)
        self.play(x, y)

    def get_value(self, color):
        score = self.get_number(Config.BLACK) - self.get_number(Config.WHITE)
        if score == 0:
            return 0.5
        elif color * score > 0:
            return 2
        else:
            return 0

    def get_number(self, color=None):
        if color is None:
            color = self.color
        num = 0
        for i in range(Config.SIZE):
            for j in range(Config.SIZE):
                if self.board[i, j] == color:
                    num += 1
        return num

    def get_score(self, color=None):
        if color is None:
            color = self.color
        return sum(sum(self.board * Config.WEIGHTS)) * color

    def is_finish(self):
        return self.get_valid_moves(Config.BLACK) == [] and self.get_valid_moves(Config.WHITE) == []

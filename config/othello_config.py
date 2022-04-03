from enum import Enum

import numpy as np


class OthelloConfig(object):
    INF = 0x3f3f3f3f
    SIZE = 8
    BLACK = 1
    WHITE = -1
    EMPTY = 0
    DIR = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
    EMPTY_BOARD = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, -1, 1, 0, 0, 0],
        [0, 0, 0, 1, -1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ], dtype=np.int8)
    WEIGHTS = np.array([
        [20, -3, 11, 8, 8, 11, -3, 20],
        [-3, -7, -4, 1, 1, -4, -7, -3],
        [11, -4, 2, 2, 2, 2, -4, 11],
        [8, 1, 2, -3, -3, 2, 1, 8],
        [8, 1, 2, -3, -3, 2, 1, 8],
        [11, -4, 2, 2, 2, 2, -4, 11],
        [-3, -7, -4, 1, 1, -4, -7, -3],
        [20, -3, 11, 8, 8, 11, -3, 20]
    ])
    ALPHA_BETA_MAX_DEPTH = 4
    ALPHA_BETA_MAX_TIME = 3
    UCT_MAX_TIME = 3
    UCB_EXPLORE = 1.414
    UCB_USE = 0


class PlayerType(Enum):
    RANDOM = "random"
    GREEDY_NUMBER = "number"
    GREEDY_SCORE = "score"
    ALPHA_BETA = "alpha_beta"
    UCT = "uct"
    DEEP_LEARNING = "deep_learning"
    LOCAL_PLAYER = "local_player"
    ONLINE_PLAYER = "online_player"
    UNKNOWN = "unknown"


class Winner(Enum):
    BLACK = "black"
    WHITE = "white"
    DRAW = "draw"

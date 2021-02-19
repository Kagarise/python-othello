import numpy as np


class OthelloConfig(object):
    INF = 0x3f3f3f3f
    SIZE = 8
    BLACK = 1
    WHITE = -1
    EMPTY = 0
    DIR = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
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
    MINIMAX_MAX_DEPTH = 4


class PlayerType(object):
    RANDOM = "random"
    GREEDY_NUMBER = "number"
    GREEDY_SCORE = "score"
    MINIMAX = "minimax"
    UCT = "uct"
    DEEP_LEARNING = "deep_learning"

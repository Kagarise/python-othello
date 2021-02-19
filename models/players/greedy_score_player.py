import random

from config.othello_config import OthelloConfig as Config
from models.game import Game
from models.player import Player


class GreedyScorePlayer(Player):
    def get_action(self, board, color):
        game = Game(board)
        moves = game.get_valid_moves(color)
        x = y = -1
        if len(moves) == 0:
            return x, y
        max_score = -Config.INF
        for v in moves:
            next_game = Game(board.copy())
            state = next_game.place(v[0], v[1], color)
            if state is False:
                return None, None
            score = next_game.get_score(color)
            if score > max_score:
                max_score = score
                # x, y = v
        best_moves = []
        for v in moves:
            next_game = Game(board.copy())
            state = next_game.place(v[0], v[1], color)
            if state is False:
                return None, None
            score = next_game.get_score(color)
            if score == max_score:
                best_moves.append(v)
        # return x, y
        return random.choice(best_moves)

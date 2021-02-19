import random

from models.game import Game
from models.player import Player


class RandomPlayer(Player):
    def get_action(self, board, color):
        game = Game(board)
        moves = game.get_valid_moves(color)
        if len(moves) == 0:
            return -1, -1
        x, y = random.choice(moves)
        return x, y

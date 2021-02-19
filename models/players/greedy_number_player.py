from models.game import Game
from models.player import Player


class GreedyNumberPlayer(Player):
    def get_action(self, board, color):
        game = Game(board)
        moves = game.get_valid_moves(color)
        x = y = -1
        if len(moves) == 0:
            return x, y
        max_num = -1
        for v in moves:
            next_game = Game(board.copy())
            state = next_game.place(v[0], v[1], color)
            if state is False:
                return None, None
            cnt = next_game.get_number(color)
            if cnt > max_num:
                max_num = cnt
                x, y = v
        return x, y

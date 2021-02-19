from config.othello_config import OthelloConfig as Config
from models.game import Game
from models.player import Player


class AlphaBetaPlayer(Player):
    def get_action(self, board, color):
        score, move = self.alpha_beta(board, Config.MINIMAX_MAX_DEPTH, -Config.INF, Config.INF, color, color,
                                      Config.MINIMAX_MAX_DEPTH)
        x, y = move
        return x, y

    @staticmethod
    def alpha_beta(board, depth, alpha, beta, current_color, color, max_depth):
        game = Game(board.copy())
        moves, states = game.get_valid_moves(current_color, True)
        if len(moves) == 0:
            return game.get_score(current_color), (-1, -1)
        if depth == 0:
            return game.get_score(current_color), (None, None)
        if depth == max_depth:
            for v in moves:
                if Config.WEIGHTS[v[0], v[1]] == Config.WEIGHTS[0, 0]:
                    return Config.INF, v
        best_move = (None, None)
        best_score = -Config.INF
        for i in range(len(states)):
            score, move = AlphaBetaPlayer.alpha_beta(states[i], depth - 1, -beta, -max(alpha, best_score),
                                                     -current_color,
                                                     color, max_depth)
            # print({"score": score, "move": move})
            score = -score
            if score > best_score:
                best_score = score
                best_move = moves[i]
                if best_score > beta:
                    return best_score, best_move
        return best_score, best_move

    def test_get_action(self, board, color):
        score, move = self.test_alpha_beta(board, Config.MINIMAX_MAX_DEPTH, -Config.INF, Config.INF, color, color)
        x, y = move
        return x, y

    @staticmethod
    def test_alpha_beta(board, depth, alpha, beta, current_color, color):
        game = Game(board.copy())
        moves, states = game.get_valid_moves(current_color, True)
        print(moves)
        if len(moves) == 0:
            return game.get_score(current_color), (-1, -1)
        if depth == 0:
            return game.get_score(current_color), (None, None)
        if color == current_color:
            best_score = -Config.INF
            best_move = (None, None)
            for i in range(len(states)):
                score, move = AlphaBetaPlayer.test_alpha_beta(states[i], depth - 1, alpha, beta, -current_color, color)
                if best_score < score:
                    best_score = score
                    best_move = move
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            return best_score, best_move
        else:
            best_score = Config.INF
            best_move = (None, None)
            for i in range(len(states)):
                score, move = AlphaBetaPlayer.test_alpha_beta(states[i], depth - 1, alpha, beta, -current_color, color)
                if best_score > score:
                    best_score = score
                    best_move = move
                beta = min(beta, score)
                if beta <= alpha:
                    break
            return best_score, best_move

from models.game import Game
from models.players import *
from config.othello_config import OthelloConfig as Config

if __name__ == "__main__":
    black = 0
    draw = 0
    white = 0
    for i in range(10):
        game = Game()
        player1 = MinimaxPlayer()
        player2 = GreedyScorePlayer()
        color = Config.BLACK
        # cnt = 0
        while game.is_finish() is False:
            # print(game.get_valid_moves(color))
            # cnt += 1
            x, y = -1, -1
            if color == Config.BLACK:
                x, y = player1.get_action(game.board.copy(), color)
            else:
                x, y = player2.get_action(game.board.copy(), color)
            # if color == Config.BLACK:
            #     print({"x": x, "y": y})
            game.place(x, y, color)
            color = -color
        # print({"cnt": cnt})
        b, w = game.get_number()
        if b - w > 0:
            print({"round": i + 1, "winner": "black"})
            black += 1
        elif b - w == 0:
            print({"round": i + 1, "winner": "draw"})
            draw += 1
        else:
            print({"round": i + 1, "winner": "white"})
            white += 1
    print({"black": black, "draw": draw, "white": white})

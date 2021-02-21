from models.game import Game
from models.players import *
from config.othello_config import OthelloConfig as Config

if __name__ == "__main__":
    black = 0
    draw = 0
    white = 0
    for i in range(20):
        game = Game()
        player1 = UCTPlayer()
        player2 = AlphaBetaPlayer()
        color = Config.BLACK
        step = 0
        while game.is_finish() is False:
            step += 1
            # print({"step": step})
            x, y = -1, -1
            if color == Config.BLACK:
                x, y = player1.get_action(game.board.copy(), color)
            else:
                x, y = player2.get_action(game.board.copy(), color)
            game.place(x, y, color)
            color = -color
        b, w = game.get_number()
        if b - w > 0:
            print({"round": i + 1, "winner": "black", "black/white": (str(b) + "/" + str(w))})
            black += 1
        elif b - w == 0:
            print({"round": i + 1, "winner": "draw", "black/white": (str(b) + "/" + str(w))})
            draw += 1
        else:
            print({"round": i + 1, "winner": "white", "black/white": (str(b) + "/" + str(w))})
            white += 1
    print({"black": black, "draw": draw, "white": white})

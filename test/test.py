from models.game import Game
from models.players import *
from config.othello_config import OthelloConfig as Config

if __name__ == "__main__":
    black = 0
    draw = 0
    white = 0
    for i in range(100):
        game = Game()
        player1 = AlphaBetaPlayer()
        player2 = GreedyScorePlayer()
        color = Config.BLACK
        while game.is_finish() is False:
            x, y = -1, -1
            if color == Config.BLACK:
                x, y = player1.get_action(game.board.copy(), color)
            else:
                x, y = player2.get_action(game.board.copy(), color)
            if color == Config.BLACK and x == -1 and y == -1 and game.get_valid_moves(color) != []:
                print("ERROR")
            game.place(x, y, color)
            color = -color
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

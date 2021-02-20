from config.othello_config import OthelloConfig
from models.players.UCT_player import State, Node, UCT

if __name__ == "__main__":
    state = State(OthelloConfig.EMPTY_BOARD, OthelloConfig.BLACK)
    # node = Node(state)
    # print(node.children)
    uct = UCT()
    result = uct.uct_search(state)
    print(result)

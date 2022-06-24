
from mcts.node import Node as MCTSNode
from mcts.monte_carlo_tree_search import MonteCarloTreeSearch
from mini_max.mini_max import MiniMax
from mini_max.mini_max import Node as MMNode
from quarto.state import State, Action
from quarto.piece import Piece, Color


class Player:
    def __init__(self):
        pass

    def select_action(self, state):
        pass


class MiniMaxPlayer(Player):
    def __init__(self, depth: int):
        super().__init__()
        self.depth = depth

    def select_action(self, state: State):
        root_node: MMNode = MNode(state=state)
        action = MiniMax.nega_max_select_action(root_node, depth=self.depth)
        return action

class MNode(MMNode):
    def __init__(self, state: State):
        super().__init__(state=state)

    # 評価関数　適当に実装
    @classmethod
    def evaluate(cls, state, depth_limit=0):
        pass


class MCTSPlayer(Player):
    def __init__(self, expand_base: int, simulation: int):
        super().__init__()
        self.expand_base = expand_base
        self.simulation = simulation

    def select_action(self, state):
        root_node: MCTSNode = MCTSNode(state, expand_base=self.expand_base)
        MonteCarloTreeSearch.train(root_node=root_node, simulation=self.simulation)
        action = MonteCarloTreeSearch.select_action(root_node)
        return action



class RandomPlayer(Player):
    def __init__(self):
        super().__init__()

    def select_action(self, state):
        action = state.random_action()
        return action


class HumanPlayer(Player):
    def __init__(self):
        super().__init__()
        self._char_dict = {
            1: '①', 2: '②', 3: '③', 4: '④',
            5: '⑤', 6: '⑥', 7: '⑦', 8: '⑧',
            9: '⑨', 10: '⑩', 11: '⑪', 12: '⑫',
            13: '⑬', 14: '⑭', 15: '⑮', 16: '⑯'
        }

    def select_action(self, state):
        piece_x, piece_y = self._input_piece_coord(state)
        input_piece_idx = self._input_piece_idx(state)
        action = Action(coord=(piece_x, piece_y), enemy_piece_idx=input_piece_idx)
        return action

    def _input_piece_idx(self, state):

        index_ret = 'remaining pieces index: '
        piece_ret = '                      : '
        available_piece_idx = []
        for idx, piece in enumerate(state.pieces):
            index_ret += self._char_dict[idx+1] + ' '

            if piece.is_available() and idx != state.selected_piece_id:
                piece_ret += str(piece) + ' '
                available_piece_idx.append(idx)
            else:
                piece_ret += 'ー' + ' '

        if len(available_piece_idx) == 0:
            return -1

        print('<< select piece >>')
        print(index_ret)
        print(piece_ret)

        input_piece_idx = int(input('Enter piece index = '))
        input_piece_idx -= 1

        if 0 <= input_piece_idx < len(state.pieces):
            if input_piece_idx in available_piece_idx:
                print()
                return input_piece_idx

        print(Color.YELLOW + 'Invalid piece index ...' + Color.END)
        print()
        return self._input_piece_idx(state)

    def _input_piece_coord(self, state):
        if state.selected_piece_id == -1:
            return -1, -1

        piece_icon = str(state.pieces[state.selected_piece_id])
        print('<< select coord >> ')
        print("selected piece -> " + piece_icon)

        piece_x, piece_y = list(map(int, input('Enter piece (x, y) = ').split()))
        piece_x -= 1
        piece_y -= 1

        if 0 <= piece_x < Piece.BOARD_WIDTH and 0 <= piece_y < Piece.BOARD_HEIGHT:
            if (piece_x, piece_y) in state.get_no_used_coords():
                print()
                return piece_x, piece_y

        print(Color.YELLOW + 'Invalid piece coord ...' + Color.END)
        print()
        return self._input_piece_coord(state)

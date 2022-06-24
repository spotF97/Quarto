import numpy as np
import dataclasses
from typing import Tuple, List
from enum import Enum, auto, unique
import copy
import random
from abstract.state import State as AState
from quarto.piece import Piece


@unique
class GameStatus(Enum):
    win = auto()
    lose = auto()
    draw = auto()
    playing = auto()

@dataclasses.dataclass(frozen=True)
class Action:
    coord: Tuple[int, int] = (-1, -1)
    enemy_piece_idx: int = -1


class State(AState):
    def __init__(self, pieces=None, selected_piece_id=-1):
        self.pieces = pieces

        self.selected_piece_id = selected_piece_id         # 相手が指定した駒のidx

        self.game_status = GameStatus.playing
        self.done = False
        if self.pieces is not None:
            self.check()

    # 駒の置いていない座標
    def get_no_used_coords(self) -> List[Tuple[int, int]]:
        used_coords = [(p.x, p.y) for p in self.pieces]
        no_used_coords = [(x, y) for x in range(Piece.BOARD_WIDTH) for y in range(Piece.BOARD_HEIGHT)
                          if (x, y) not in (set(used_coords))]
        return no_used_coords

    def legal_actions(self) -> list:

        # 駒の置いていない座標
        no_used_coords = self.get_no_used_coords()

        # 相手に渡せる駒のidx
        available_pieces = [idx for idx, p in enumerate(self.pieces)
                            if p.is_available() and idx != self.selected_piece_id]

        # 先手で相手の駒を選ぶとき
        if self.selected_piece_id == -1:
            las = [Action(enemy_piece_idx=p_idx) for p_idx in available_pieces]

        # 渡せる駒がない、つまり最後に駒を置くとき
        elif not available_pieces:
            las = [Action(coord=coord) for coord in no_used_coords]

        # 通常時
        else:
            las = [Action(coord=coord, enemy_piece_idx=p_idx) for p_idx in available_pieces for coord in no_used_coords]

        return las

    def random_action(self):
        las = self.legal_actions()
        return random.choice(las)

    def next(self, action: Action):

        n_pieces = copy.deepcopy(self.pieces)

        # 駒を動かす　（action.coord is None）
        if self.selected_piece_id != -1:
            target_piece = n_pieces[self.selected_piece_id]
            target_piece.x, target_piece.y = action.coord

        n_state = State(pieces=n_pieces, selected_piece_id=action.enemy_piece_idx)

        return n_state

    def is_lose(self) -> bool:
        return self.game_status == GameStatus.win

    def is_draw(self) -> bool:
        return self.game_status == GameStatus.draw

    def is_done(self) -> bool:
        return self.done

    def is_first_player(self) -> bool:
        # 駒の選択が先手
        if self.selected_piece_id == -1:
            return True

        n_pieces = sum(p.is_available() for p in self.pieces)
        return n_pieces % 2 != 0

    def initialize(self):
        # 駒
        self.pieces = []
        for color in [Piece.BLACK, Piece.WHITE]:
            for shape in [Piece.SQUARE, Piece.ROUND]:
                for hole in [Piece.HAVE_HOLE, Piece.NO_HOLE]:
                    for height in [Piece.L, Piece.H]:
                        piece = Piece(color, shape, hole, height)
                        self.pieces.append(piece)

    # 揃っているか
    @staticmethod
    def _check_quarto(board):
        for attr in [Piece.attr1, Piece.attr2]:
            for i in range(Piece.BOARD_SIZE):
                # 縦が揃っているか
                if np.all(board[:, i] == attr):
                    return True

                # 横が揃っているか
                if np.all(board[i, :] == attr):
                    return True

            # 斜めが揃っているか
            if np.all(np.diag(board) == attr) or np.all(np.diag(np.fliplr(board)) == attr):
                return True

        return False

    # 勝敗の判定
    def check(self):

        # 盤面の状態
        shape = np.zeros((Piece.BOARD_HEIGHT, Piece.BOARD_WIDTH))
        color = np.zeros((Piece.BOARD_HEIGHT, Piece.BOARD_WIDTH))
        height = np.zeros((Piece.BOARD_HEIGHT, Piece.BOARD_WIDTH))
        hole = np.zeros((Piece.BOARD_HEIGHT, Piece.BOARD_WIDTH))

        for p in self.pieces:
            if not p.is_available():
                shape[p.y][p.x] = p.shape
                color[p.y][p.x] = p.color
                height[p.y][p.x] = p.height
                hole[p.y][p.x] = p.hole

        # 各属性についてタテ・ヨコ・ナナメ揃っているものがあるか
        for attr_type in [shape, color, height, hole]:
            if self._check_quarto(attr_type):
                self.game_status = GameStatus.win
                self.done = True
                return

        # 駒が全て置かれているか
        if np.all(shape != 0):
            self.game_status = GameStatus.draw
            self.done = True
            return

        # self.done = False

    def __str__(self):
        board = [['ー' for _ in range(Piece.BOARD_WIDTH)] for _ in range(Piece.BOARD_HEIGHT)]
        ret = ''
        # color = [[0]*4]*4
        # board = '-' * 16

        ret += '　１２３４' + '\n'


        for piece in self.pieces:
            if not piece.is_available():
                board[piece.y][piece.x] = str(piece)
                # board[piece.x + piece.y*4] = str(piece)

        for y in range(Piece.BOARD_HEIGHT):
            ret += str(y+1) + ' '
            for x in range(Piece.BOARD_WIDTH):
                ret += board[y][x]

            ret += '\n'

        return ret

    """
    def how2win(self, dict_win):

        shape = np.zeros((BOARD_HEIGHT, BOARD_WIDTH))
        color = np.zeros((BOARD_HEIGHT, BOARD_WIDTH))
        height = np.zeros((BOARD_HEIGHT, BOARD_WIDTH))
        hole = np.zeros((BOARD_HEIGHT, BOARD_WIDTH))


        for p in self.pieces:
            if not p.is_available():
                shape[p.y][p.x] = p.shape
                color[p.y][p.x] = p.color
                height[p.y][p.x] = p.height
                hole[p.y][p.x] = p.hole

        # 各属性についてタテ・ヨコ・ナナメ揃っているものがあるか
        for type, type_str in zip([shape, color, height, hole], ["shape", "color", "height", "hole"]):
            for attr in [attr1, attr2]:
                for i in range(BOARD_SIZE):
                    # 縦が揃っているか
                    if np.all(type[:, i] == attr):
                        count = dict_win.get(type_str, 0)
                        dict_win[type_str] = count + 1

                    # 横が揃っているか
                    if np.all(type[i, :] == attr):
                        count = dict_win.get(type_str, 0)
                        dict_win[type_str] = count + 1

                # 斜めが揃っているか
                if np.all(np.diag(type) == attr) or np.all(np.diag(np.fliplr(type)) == attr):
                    count = dict_win.get(type_str, 0)
                    dict_win[type_str] = count + 1

        return dict_win


    def n_call(self):

        ptypes = []
        # 揃っているか

        def aligned(boards):
            count_call = 0

            b3, b4 = True, True
            for i in range(BOARD_SIZE):

                b1, b2 = True, True
                for board, ptype in zip(boards, ['shape', 'color', 'height', 'hole']):
                    for attr in [attr1, attr2]:
                        # 縦が揃っているか
                        if np.sum(board[:, i] == attr) == 3:
                            if b1:
                                count_call += 1
                                b1 = False

                            ptypes.append(Attribute(ptype, attr))

                        # 横が揃っているか
                        if np.sum(board[i, :] == attr) == 3:
                            if b2:
                                count_call += 1
                                b2 = False

                            ptypes.append(Attribute(ptype, attr))

                        # 斜めが揃っているか
                        if np.sum(np.diag(board) == attr) == 3:
                            if b3:
                                count_call += 1
                                b3 = False

                            ptypes.append(Attribute(ptype, attr))

                        if np.sum(np.diag(np.fliplr(board)) == attr) == 3:
                            if b4:
                                count_call += 1
                                b4 = False

                            ptypes.append(Attribute(ptype, attr))

            return count_call


        shape = np.zeros((BOARD_HEIGHT, BOARD_WIDTH))
        color = np.zeros((BOARD_HEIGHT, BOARD_WIDTH))
        height = np.zeros((BOARD_HEIGHT, BOARD_WIDTH))
        hole = np.zeros((BOARD_HEIGHT, BOARD_WIDTH))

        for p in self.pieces:
            if not p.is_available():
                shape[p.y][p.x] = p.shape
                color[p.y][p.x] = p.color
                height[p.y][p.x] = p.height
                hole[p.y][p.x] = p.hole

        # 各属性についてタテ・ヨコ・ナナメ揃っているものがあるか
        # for type in [shape, color, height, hole]:
        #    n_calls += aligned(type)
        n_calls = aligned([shape, color, height, hole])

        return n_calls, ptypes
        """

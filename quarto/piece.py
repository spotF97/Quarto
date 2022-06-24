
class Color:
    RED = '\033[31m'        # (文字)赤
    GREEN = '\033[32m'      # (文字)緑
    YELLOW = '\033[33m'     # (文字)黄
    END = '\033[0m'


class GameInfo:
    P1 = 0      # 先手 / 白(赤)
    P2 = 1      # 後手 / 黒(緑)

    BOARD_HEIGHT = 4
    BOARD_WIDTH = 4
    BOARD_SIZE = 4

    attr1 = 1
    attr2 = 2

    WHITE = attr1
    BLACK = attr2

    SQUARE = attr1
    ROUND = attr2

    HAVE_HOLE = attr1
    NO_HOLE = attr2

    L = attr1
    H = attr2



class Piece(GameInfo):
    def __init__(self, color, shape, hole, height):
        self.color = color
        self.shape = shape
        self.hole = hole
        self.height = height
        self.x = -1
        self.y = -1
        self.type = self.set_Type()

    """ 使っていない駒か """
    def is_available(self):
        return (self.x == -1) and (self.y == -1)

    def set_Type(self):
        sh = 'square' if self.shape == Piece.SQUARE else 'round'
        ho = 'perforated' if self.hole == Piece.HAVE_HOLE else 'Not perforated'
        he = 'H' if self.height == Piece.H else 'L'
        co = 'W' if self.color == Piece.WHITE else 'B'

        return f'{co} _ {ho} _ {sh} _ {he}'
        # return self.color + ho + sh + he

    def __str__(self):
        color = Color.RED if self.color == Piece.WHITE else Color.GREEN

        if self.shape == Piece.SQUARE:
            if self.hole == Piece.HAVE_HOLE:
                piece_str = '🄷' if self.height == Piece.H else '🄻'
            else:
                piece_str = '🅷' if self.height == Piece.H else '🅻'
        else:
            if self.hole == Piece.HAVE_HOLE:
                piece_str = 'Ⓗ' if self.height == Piece.H else 'Ⓛ'
            else:
                piece_str = '🅗' if self.height == Piece.H else '🅛'

        return color + piece_str + Color.END


    def __eq__(self, other):
        if not isinstance(other, Piece):
            return NotImplemented

        if (self.color != other.color) or (self.shape != other.shape) or\
                (self.hole != other.hole) or (self.height != other.height):
            return False

        if (self.x != other.x) or (self.y != other.y):
            return False

        return True

    def __hash__(self):
        return hash((self.color, self.height, self.hole, self.shape, self.x, self.y))

    """ 駒の属性の取得 """
    def get_type(self, ptype):
        if ptype == 'color':
            return self.color
        elif ptype == 'height':
            return self.height
        elif ptype == 'hole':
            return self.hole
        elif ptype == 'shape':
            return self.shape
        else:
            return None

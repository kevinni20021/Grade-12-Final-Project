from Pieces import Piece
from Pieces import Bishop, King, Queen, Pawn, Rook, Knight
import pygame as py
import math
from typing import Optional, Any, Union
from copy import deepcopy

_MASTER_PRE_MOVE_STATE = []
_MASTER_POST_MOVE_STATE = []
SCREEN_WIDTH = 512
SCREEN_HEIGHT = 512
SQUARES = 8
SQUARE_SIZE = SCREEN_HEIGHT // SQUARES
IMAGES = {}
PIECES = ["bR", "bN", "bB", "bQ", "bP", "bK", "wR", "wN", "wB", "wQ", "wP",
          "wK"]
PIECE_DIRECTORY = {'B': Bishop, 'Q': Queen, 'N': Knight,
                   'K': King, 'P': Pawn, 'R': Rook}
COLOURS = [py.Color("tan"), py.Color("brown")]
COORD_X_DICT = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
REVERSED_COORD_X_DICT = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6,
                         'h': 7}
COORD_Y_DICT = {0: 8, 1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1}
REVERSED_COORD_Y_DICT = {8: 0, 7: 1, 6: 2, 5: 3, 4: 4, 3: 5, 2: 6, 1: 7}


class _BoardState:
    """
    a board state within the move log
    """
    next: Optional[Any]
    prev: Optional[Any]
    item: Optional[Any]

    def __init__(self, item: Any) -> None:
        self.item = item
        self.next = None
        self.prev = None

    def get_board(self) -> Any:
        return self.item


class MoveLog:
    """
    a linked list implementation of a move log

    """
    _first: Optional[_BoardState]
    item: Optional[_BoardState]

    def __init__(self) -> None:
        self._first = None
        self.curr = self._first

    def __len__(self) -> int:
        counter = 0
        curr = self._first
        while curr is not None:
            curr = curr.next
            counter += 1
        return counter

    def __str__(self) -> str:
        curr = self._first
        i = 0
        final = ""
        while curr is not None:
            if i % 2 == 0:
                final += " {}.".format(math.ceil(i / 2 + 0.1))
                i += 1
            else:
                i += 1
            final += str(curr.item)
            curr = curr.next
        return final

    def append(self, item: any) -> None:
        curr = self._first
        if curr is None:
            self._first = _BoardState(item)
        else:
            while curr.next is not None:
                curr = curr.next
            curr.next = _BoardState(item)


class Board:
    """
    Setup the chess board, loads the images, draws the board and pieces
    ==== Public Attributes ===
    white_to_move:
        If it is white's turn to move
    move_log:
        a list of all moves
    board:
        a dictionary of the pieces of coordinates
    selected:
        the currently selected piece and location
    """
    board: dict[int, dict[str, Any]]
    move_log: MoveLog
    _board_states: list
    _move_count: int
    white_to_move: bool
    selected: bool

    def __init__(self) -> None:
        """
        Initialize the Board and each attribute
        """
        self.board = {
            8: {"a": "bR", "b": "bN", "c": "bB", "d": "bQ", "e": "bK",
                "f": "bB", "g": "bN", "h": "bR"},
            7: {"a": "bP", "b": "bP", "c": "bP", "d": "bP", "e": "bP",
                "f": "bP", "g": "bP", "h": "bP"},
            6: {"a": "", "b": "", "c": "", "d": "", "e": "", "f": "", "g": "",
                "h": ""},
            5: {"a": "", "b": "", "c": "", "d": "", "e": "", "f": "", "g": "",
                "h": ""},
            4: {"a": "", "b": "", "c": "", "d": "", "e": "", "f": "", "g": "",
                "h": ""},
            3: {"a": "", "b": "", "c": "", "d": "", "e": "", "f": "", "g": "",
                "h": ""},
            2: {"a": "wP", "b": "wP", "c": "wP", "d": "wP", "e": "wP",
                "f": "wP", "g": "wP", "h": "wP"},
            1: {"a": "wR", "b": "wN", "c": "wB", "d": "wQ", "e": "wK",
                "f": "wB", "g": "wN", "h": "wR"}
        }
        self.white_to_move = True
        self.selected = False
        self._move_count = 0
        self.move_log = MoveLog()
        self._board_states = []
        _MASTER_PRE_MOVE_STATE.append(deepcopy(self))
        _MASTER_POST_MOVE_STATE.append(deepcopy(self))

    def load_images(self, pieces: list[str]) -> None:
        """
        loads the images for every piece
        :param pieces: list of pieces
        """
        for piece in pieces:
            IMAGES[piece] = py.transform.scale(
                py.image.load("Images/" + piece + ".png"),
                (SQUARE_SIZE, SQUARE_SIZE))

    def draw_board(self, screen: py.display, palette: list[py.Color]) -> None:
        """
        Draws an 8 x 8 chess board with the proper colours

        :param screen: the screen that we are drawing the board one
        :param palette: the first colour is the colour for white, second is for black
        :return: None
        """
        colours = [py.Color(palette[0]), py.Color(palette[1])]
        for row in range(SQUARES):
            for column in range(SQUARES):
                colour = colours[((row + column) % 2)]
                py.draw.rect(screen, colour,
                             py.Rect(column * SQUARE_SIZE, row * SQUARE_SIZE,
                                     SQUARE_SIZE, SQUARE_SIZE))

    def set_up_pieces(self) -> None:
        """
        set up and instantiate each piece and their respective classes
        """
        i = 1
        while i <= SQUARES:
            temp_list = list(self.board[i].values())
            temp_list2 = list(self.board[i].keys())
            for column in range(SQUARES):
                if temp_list[column] in PIECES:
                    position = ((temp_list2[column]), i)
                    curr = PIECE_DIRECTORY[
                        self.board[i][temp_list2[column]][1]](
                        self.board[i][temp_list2[column]][0], position)
                    self.board[i][temp_list2[column]] = curr
            i += 1

    def draw_pieces(self, screen: py.display) -> None:
        """
        draws the pieces on to the board
        :param screen: screen to draw the pieces on
        :return: None
        """
        i = 1
        while i <= SQUARES:
            temp_list = list(self.board[i].values())
            for column in range(SQUARES):
                if str(temp_list[column]) in PIECES:
                    piece = str(temp_list[column])
                    screen.blit(IMAGES[piece],
                                py.Rect(column * SQUARE_SIZE,
                                        (SQUARES - i) * SQUARE_SIZE,
                                        SQUARE_SIZE, SQUARE_SIZE))
            i += 1

    def get_piece(self, coord_x, coord_y) -> Union[
        King, Bishop, Knight, Rook, Pawn, Queen]:
        coord_x = int(math.floor(coord_x / 64))
        coord_y = int(math.floor(coord_y / 64))
        x = COORD_X_DICT[coord_x]
        y = COORD_Y_DICT[coord_y]

        return self.board[y][x]

    def move_piece(self, piece: Union[King, Bishop, Knight, Rook, Pawn, Queen],
                   old_pos, new_pos, screen) -> None:
        """
        moves the piece to the new
        :param piece: the piece to be moved
        :param old_pos: current position of the piece (where the piece is moving
                        from)
        :param new_pos: new position of the piece (where the piece is moving to)
        :param screen:
        """
        moved_piece = piece
        _MASTER_PRE_MOVE_STATE.insert(self._move_count, deepcopy(self))
        self._move_count += 1
        for i in range(len(_MASTER_PRE_MOVE_STATE) - self._move_count - 1):
            _MASTER_PRE_MOVE_STATE.pop()
        if isinstance(self.board[new_pos[1]][new_pos[0]], Piece):
            # captured_piece = self.board[new_pos[1]][new_pos[0]]
            self.move_log.append(f"{str(moved_piece)[1]}"
                                 f"{moved_piece.get_current_position()[0]}x"
                                 f"{new_pos[0]}"
                                 f"{new_pos[1]}")
        else:
            self.move_log.append(f"{str(piece)[1]}{new_pos[0]}{new_pos[1]}")
        self.board[old_pos[1]][old_pos[0]] = ""
        self.board[new_pos[1]][new_pos[0]] = moved_piece
        moved_piece.position = (new_pos[0], new_pos[1])
        _MASTER_POST_MOVE_STATE.insert(self._move_count, deepcopy(self))
        for i in range(len(_MASTER_POST_MOVE_STATE) - self._move_count - 1):
            _MASTER_POST_MOVE_STATE.pop()
        self.update(screen)

    def update(self, screen: py.display) -> None:
        """
        updates the board
        :param screen: screen to draw the pieces on
        """
        self.draw_board(screen, COLOURS)
        self.set_up_pieces()
        self.draw_pieces(screen)
        py.display.flip()

    def undo(self) -> Any:
        print(f"you undid {self._move_count}")
        if self._move_count > 0:
            return _MASTER_PRE_MOVE_STATE[self._move_count - 1]
        else:
            return self

    def redo(self) -> Any:
        print(f"you redid {self._move_count + 1}")
        if self._move_count + 1 < len(_MASTER_POST_MOVE_STATE):
            return _MASTER_POST_MOVE_STATE[self._move_count + 1]
        else:
            return self

    def _record(self):
        return self

    def generate_all_valid_moves(self) -> list[
        dict[str, dict[tuple[str, str], list[str, int]]]]:
        b_valid_moves = {}
        w_valid_moves = {}
        for cord_1 in self.board.keys():
            for cord_2, piece in self.board[cord_1].items():
                if piece == '':
                    pass
                elif 'b' in piece.colour:
                    b_valid_moves[(
                    str(piece), cord_2 + str(cord_1))] = piece.get_valid_moves(
                        board=self.board,
                        coord_x=REVERSED_COORD_X_DICT[cord_2] * 64,
                        coord_y=REVERSED_COORD_Y_DICT[cord_1] * 64,
                        move=self.white_to_move)
                elif 'w' in piece.colour:
                    w_valid_moves[(
                    str(piece), cord_2 + str(cord_1))] = piece.get_valid_moves(
                        board=self.board,
                        coord_x=REVERSED_COORD_X_DICT[cord_2] * 64,
                        coord_y=REVERSED_COORD_Y_DICT[cord_1] * 64,
                        move=self.white_to_move)
        return [{"Black": b_valid_moves}, {"White": w_valid_moves}]

    def prettier_all_move(self):
        valid = self.generate_all_valid_moves()

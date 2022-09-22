from typing import Optional
import math

SQUARES = 64
COORD_X_DICT = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
COORD_Y_DICT = {0: 8, 1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1}
BOARD_RANGE = range(1, 511)
direction = [1, -1]


class Piece:
    """
    This is a abstract class for a chess piece
    ====Public Attributes====
    colour:
        black or white coloured piece
    is_selected:
        indicates if the piece has been selected by the player
    position:
        the current position of the piece
    opposite colour:
        the opposite colour of the piece, if the piece is white the opposite
        colour would be black and vice versa.
    """
    colour: str
    is_selected: bool
    position: tuple[str, int]
    opposite_colour: str

    def __init__(self, colour: str, position: tuple[str, int]) -> None:
        """
        Initializes the Piece and its attributes
        :param colour: colour of the piece
        :param position: position where it is initialized
        """
        self.colour = colour
        self.is_selected = False
        self.position = position
        if self.colour == 'w':
            self.opposite_colour = 'b'
        elif self.colour == 'b':
            self.opposite_colour = 'w'

    def get_current_position(self) -> tuple[str, int]:
        """
        return the current position of the piece
        """
        return self.position

    def get_valid_moves(self, board, coord_x, coord_y, move) -> \
            list[tuple[str, int]]:
        """
        This is an abstract method
        Returns a list of moves that are valid for the current piece
        :param board: the board
        :param coord_x: the x / letter component of the piece position
        :param coord_y: the y / number component of the piece position
        :param move: if the piece is allowed to move
        :return: a list of valid moves
        """
        raise NotImplementedError

    def get_colour(self):
        return self.colour

    def __str__(self) -> str:
        if type(self) == King:
            return "{}K".format(self.colour)
        elif type(self) == Queen:
            return "{}Q".format(self.colour)
        elif type(self) == Pawn:
            return "{}P".format(self.colour)
        elif type(self) == Knight:
            return "{}N".format(self.colour)
        elif type(self) == Bishop:
            return "{}B".format(self.colour)
        elif type(self) == Rook:
            return "{}R".format(self.colour)


def get_coordinates(coord_x, coord_y) -> tuple[str, int]:
    coord_x = int(math.floor(coord_x / 64))
    coord_y = int(math.floor(coord_y / 64))
    x = COORD_X_DICT[coord_x]
    y = COORD_Y_DICT[coord_y]
    final = (str(x), y)
    return final


class King(Piece):
    def __init__(self, colour, position):
        Piece.__init__(self, colour, position)

    def get_valid_moves(self, board, coord_x, coord_y, move) -> \
            Optional[list[tuple[str, int]]]:
        valid_move = []
        if self.colour == 'w' and move is False:
            return valid_move
        elif self.colour == 'b' and move is True:
            return valid_move
        for num1 in direction:
            for num2 in direction:
                if coord_y - SQUARES * num1 in BOARD_RANGE and \
                        coord_x - SQUARES * num2 in BOARD_RANGE:
                    curr = get_coordinates(coord_x - SQUARES * num2,
                                           coord_y - SQUARES * num1)
                    if board[curr[1]][curr[0]] == "":
                        valid_move.append(curr)
                    elif self.opposite_colour in str(
                            board[curr[1]][curr[0]]):
                        valid_move.append(curr)

            if coord_y + SQUARES * num1 in BOARD_RANGE:
                vertical = get_coordinates(coord_x, coord_y + SQUARES * num1)
                if board[vertical[1]][vertical[0]] == "":
                    valid_move.append(vertical)
                elif self.opposite_colour in str(
                        board[vertical[1]][vertical[0]]):
                    valid_move.append(vertical)

            if coord_x + SQUARES * num1 in BOARD_RANGE:
                side = get_coordinates(coord_x + SQUARES * num1, coord_y)
                if board[side[1]][side[0]] == "":
                    valid_move.append(side)
                elif self.opposite_colour in str(board[side[1]][side[0]]):
                    valid_move.append(side)
        return valid_move


class Queen(Piece):
    def __init__(self, colour, position):
        Piece.__init__(self, colour, position)

    def get_valid_moves(self, board, coord_x, coord_y, move) -> \
            list[tuple[str, int]]:
        valid_move = []
        if self.colour == 'w' and move is False:
            return valid_move
        elif self.colour == 'b' and move is True:
            return valid_move
        for nums1 in direction:
            for nums2 in direction:
                for rows in range(1, 8):
                    if coord_y - SQUARES * rows * nums1 in BOARD_RANGE \
                            and coord_x - SQUARES * rows * nums2 in BOARD_RANGE:
                        curr = get_coordinates(coord_x - SQUARES * rows * nums2,
                                               coord_y - SQUARES * rows * nums1)
                        if board[curr[1]][curr[0]] == "":
                            valid_move.append(curr)
                        elif self.opposite_colour in str(
                                board[curr[1]][curr[0]]):
                            valid_move.append(curr)
                            break
                        else:
                            break
            for rows in range(1, 8):
                if coord_y + SQUARES * rows * nums1 in BOARD_RANGE:
                    curr = get_coordinates(coord_x,
                                           coord_y + SQUARES * rows * nums1)
                    if board[curr[1]][curr[0]] == "":
                        valid_move.append(curr)
                    elif self.opposite_colour in str(
                            board[curr[1]][curr[0]]):
                        valid_move.append(curr)
                        break
                    else:
                        break
            for rows in range(1, 8):
                if coord_x + SQUARES * rows * nums1 in BOARD_RANGE:
                    curr = get_coordinates(coord_x + SQUARES * rows * nums1,
                                           coord_y)
                    if board[curr[1]][curr[0]] == "":
                        valid_move.append(curr)
                    elif self.opposite_colour in str(
                            board[curr[1]][curr[0]]):
                        valid_move.append(curr)
                        break
                    else:
                        break

        return valid_move


class Knight(Piece):
    """
    A knight chess piece, a knight can move in a
    """

    def __init__(self, colour, position):
        Piece.__init__(self, colour, position)

    def get_valid_moves(self, board, coord_x, coord_y, move) -> \
            list[tuple[str, int]]:
        valid_move = []
        if self.colour == 'w' and move is False:
            return valid_move
        elif self.colour == 'b' and move is True:
            return valid_move
        for num1 in direction:
            for num2 in direction:
                if coord_y - SQUARES * num1 * 2 in BOARD_RANGE and \
                        coord_x - SQUARES * num2 in BOARD_RANGE:
                    curr = get_coordinates(coord_x - SQUARES * num2,
                                           coord_y - SQUARES * num1 * 2)
                    if board[curr[1]][curr[0]] == "":
                        valid_move.append(curr)
                    elif self.opposite_colour in str(
                            board[curr[1]][curr[0]]):
                        valid_move.append(curr)

                if coord_y - SQUARES * num1 in BOARD_RANGE and \
                        coord_x - SQUARES * num2 * 2 in BOARD_RANGE:
                    curr = get_coordinates(coord_x - SQUARES * num2 * 2,
                                           coord_y - SQUARES * num1)
                    if board[curr[1]][curr[0]] == "":
                        valid_move.append(curr)
                    elif self.opposite_colour in str(
                            board[curr[1]][curr[0]]):
                        valid_move.append(curr)
        return valid_move


class Pawn(Piece):
    def __init__(self, colour, position):
        Piece.__init__(self, colour, position)
        if self.colour == 'b':
            self.properties = [7, -1, 'h', 'a']
        elif self.colour == 'w':
            self.properties = [2, 1, 'a', 'h']

    def get_valid_moves(self, board, coord_x, coord_y, move) -> \
            list[tuple[str, int]]:
        valid_move = []
        if self.colour == 'w' and move is False:
            return valid_move
        elif self.colour == 'b' and move is True:
            return valid_move
        if self.properties[0] in get_coordinates(coord_x, coord_y):
            valid_move.append(
                get_coordinates(coord_x,
                                coord_y - (SQUARES * 2 * self.properties[1])))
        if board[get_coordinates(coord_x, coord_y - SQUARES * self.properties[1])[
                1]][
            get_coordinates(coord_x, coord_y - SQUARES * self.properties[1])[
                0]] == "":
            valid_move.append(get_coordinates(coord_x, coord_y - SQUARES *
                                              self.properties[1]))
        # white pawn captures
        if self.properties[2] not in get_coordinates(coord_x, coord_y):
            if self.opposite_colour in str(board[get_coordinates(
                    coord_x - SQUARES * self.properties[1],
                    coord_y - SQUARES * self.properties[1])[1]][
                                               get_coordinates(
                                                   coord_x - SQUARES *
                                                   self.properties[1],
                                                   coord_y - SQUARES *
                                                   self.properties[1])[0]]):
                valid_move.append(
                    get_coordinates(coord_x - SQUARES * self.properties[1],
                                    coord_y - SQUARES * self.properties[1]))
        if self.properties[3] not in get_coordinates(coord_x, coord_y):
            if self.opposite_colour in str(board[get_coordinates(
                    coord_x + SQUARES * self.properties[1],
                    coord_y - SQUARES * self.properties[1])[1]][
                                               get_coordinates(
                                                   coord_x + SQUARES *
                                                   self.properties[1],
                                                   coord_y - SQUARES *
                                                   self.properties[1])[0]]):
                valid_move.append(
                    get_coordinates(coord_x + SQUARES * self.properties[1],
                                    coord_y - SQUARES * self.properties[1]))
        return valid_move


class Bishop(Piece):
    def __init__(self, colour, position):
        Piece.__init__(self, colour, position)

    def get_valid_moves(self, board, coord_x, coord_y, move) -> \
            list[tuple[str, int]]:
        valid_move = []
        if self.colour == 'w' and move is False:
            return valid_move
        elif self.colour == 'b' and move is True:
            return valid_move
        for nums1 in direction:
            for nums2 in direction:
                for rows in range(1, 8):
                    if coord_y - SQUARES * rows * nums1 in BOARD_RANGE \
                            and coord_x - SQUARES * rows * nums2 in BOARD_RANGE:
                        curr = get_coordinates(coord_x - SQUARES * rows * nums2,
                                               coord_y - SQUARES * rows * nums1)
                        if board[curr[1]][curr[0]] == "":
                            valid_move.append(curr)
                        elif self.opposite_colour in str(
                                board[curr[1]][curr[0]]):
                            valid_move.append(curr)
                            break
                        else:
                            break
        return valid_move


class Rook(Piece):
    def __init__(self, colour, position):
        Piece.__init__(self, colour, position)

    def get_valid_moves(self, board, coord_x, coord_y, move) -> \
            list[tuple[str, int]]:
        valid_move = []
        if self.colour == 'w' and move is False:
            return valid_move
        elif self.colour == 'b' and move is True:
            return valid_move
        for nums1 in direction:
            for rows in range(1, 8):
                if coord_y + SQUARES * rows * nums1 in BOARD_RANGE:
                    curr = get_coordinates(coord_x,
                                           coord_y + SQUARES * rows * nums1)
                    if board[curr[1]][curr[0]] == "":
                        valid_move.append(curr)
                    elif self.opposite_colour in str(
                            board[curr[1]][curr[0]]):
                        valid_move.append(curr)
                        break
                    else:
                        break
            for rows in range(1, 8):
                if coord_x + SQUARES * rows * nums1 in BOARD_RANGE:
                    curr = get_coordinates(coord_x + SQUARES * rows * nums1,
                                           coord_y)
                    if board[curr[1]][curr[0]] == "":
                        valid_move.append(curr)
                    elif self.opposite_colour in str(
                            board[curr[1]][curr[0]]):
                        valid_move.append(curr)
                        break
                    else:
                        break
        return valid_move

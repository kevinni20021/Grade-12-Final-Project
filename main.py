from Pieces import get_coordinates
from Board import Board, MoveLog, _BoardState
import pygame as py
from typing import Optional, Any, Union

SCREEN_WIDTH = 512
SCREEN_HEIGHT = 512
SQUARES = 8
SQUARE_SIZE = SCREEN_HEIGHT // SQUARES
IMAGES = {}
PIECES = ["bR", "bN", "bB", "bQ", "bP", "bK", "wR", "wN", "wB", "wQ", "wP",
          "wK"]
COLOURS = [py.Color("tan"), py.Color("brown")]


def setup(game: Board) -> None:
    """
    Sets up the game
    :param game: the board to set up
    """
    game.load_images(pieces=PIECES)
    game.draw_board(screen=screen, palette=COLOURS)
    game.set_up_pieces()
    game.draw_pieces(screen=screen)
    py.display.flip()


if __name__ == '__main__':
    print("Chess by Kevin Ni")
    py.init()
    py.display.set_caption("Chess")
    in_play = True
    game = Board()
    screen = py.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(py.Color("white"))
    setup(game)
    valid = []
    piece = None
    piece_position = None
    while in_play:
        if len(game.move_log) % 2 == 0:
            game.white_to_move = True
        else:
            game.white_to_move = False
        for event in py.event.get():
            if event.type == py.QUIT:
                in_play = False
            if event.type == py.MOUSEBUTTONDOWN:
                position_x, position_y = py.mouse.get_pos()
                a = game.get_piece(position_x, position_y)
                if a != "" and not game.selected:
                    piece = game.get_piece(position_x, position_y)
                    valid = a.get_valid_moves(game.board, position_x,
                                              position_y, game.white_to_move)
                    piece_position = a.get_current_position()
                    game.selected = True
                    game.update(screen)
                elif game.selected:
                    pos = get_coordinates(position_x, position_y)
                    if pos in valid:
                        game.move_piece(piece, piece_position, pos, screen)
                    game.selected = False
                else:
                    piece = None
                    pos = None
                    piece_position = None
                    game.selected = False
                    game.update(screen)
            if event.type == py.KEYDOWN:
                if event.key == py.K_LEFT:
                    game = game.undo()
                    game.update(screen)
                if event.key == py.K_RIGHT:
                    game = game.redo()
                    game.update(screen)
                if event.key == py.K_0:
                    all_move = game.generate_all_valid_moves()
                    if game.white_to_move:
                        print(all_move[1])
                    elif not game.white_to_move:
                        print(all_move[0])

        game.update(screen)
        py.display.flip()

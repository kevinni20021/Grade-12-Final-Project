import Pieces as p


class Player:
    """player class abstract"""
    colour: str

    def __init__(self, colour: str) -> None:
        if "w" in colour.lower():
            self.colour = 'White'
        elif 'b' in colour.lower():
            self.colour = 'Black'
        else:
            raise 'NotValidColourError'

    def make_move:
        pass


class Engine(Player):
    """
    The chess Engine
    """
    pass


class Human(Player):
    pass


class AI(Player):
    def __init__(self) -> None:
        super().__init__()

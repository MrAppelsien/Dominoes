import random
from dataclasses import dataclass
from itertools import combinations_with_replacement, cycle
from typing import Tuple, Sequence, Iterable, List


@dataclass
class DominoStone:
    nr1: int
    nr2: int

    def __lt__(self, other):
        return not self.__gt__(other)

    def __gt__(self, other):
        if self.nr2 > other.nr2:
            return True

        if self.nr2 < other.nr2:
            return False

        return self.nr1 > other.nr1

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'[{self.nr1}, {self.nr2}]'

    def is_double(self) -> bool:
        return self.nr1 == self.nr2

class GameState:
    player: str = ''

    snake: List[DominoStone] = []
    pieces_computer: List[DominoStone]
    pieces_player: List[DominoStone]
    pieces_hoop: List[DominoStone]

    @property
    def pieces(self) -> List[DominoStone]:
        if self.player == 'player':
            return self.pieces_player

        return self.pieces_computer

    @property
    def other_pieces(self) -> List[DominoStone]:
        if self.player == 'computer':
            return self.pieces_player

        return self.pieces_computer

    def switch(self):
        if self.player == 'player':
            self.player = 'computer'
        else:
            self.player = 'player'

    def play_piece(self, stuk, append=True):
        self.pieces.remove(stuk)
        self.switch()
        if not self.snake:
            self.snake.append(stuk)
            return

        if append:
            laatste_stuk = self.snake[-1]   # pak laatste dominosteen van snake
            if stuk.nr2 == laatste_stuk.nr2:     # check dat dit klopt "stuk == laatste"
                stuk.nr1, stuk.nr2 = stuk.nr2, stuk.nr1  # draai het stuk om
            self.snake.append(stuk)

        else:
            eerste_stuk = self.snake[0]   # zie comentaar hier boven
            if stuk.nr1 == eerste_stuk.nr1:
                stuk.nr1, stuk.nr2 = stuk.nr2, stuk.nr1
            self.snake.insert(0, stuk)

    def take_piece(self):
        self.switch()
        return

        # try:
        #     new_piece = random.choice(self.pieces_hoop)
        #     self.pieces.append(new_piece)
        #     self.pieces_hoop.remove(new_piece)
        # except IndexError:
        #     pass

        #self.switch()
gamestate = GameState()


class NoDoubles(Exception):
    """No doubles in either deck."""


def is_valid_for_comp():
    stuk = gamestate.pieces_computer[-1]
    if is_valid_move_comp(stuk) == "append":
        gamestate.play_piece(stuk, append=True)
    else:
        gamestate.play_piece(stuk, append=False)
def is_valid_move_comp(stuk):
    laatste_stuk = gamestate.snake[-1]
    eerste_stuk = gamestate.snake[0]

    if stuk.nr1 == laatste_stuk.nr2:
        return "append"
    if stuk.nr2 == laatste_stuk.nr2:
        return "append"

    if stuk.nr2 == eerste_stuk.nr1:
        return "prepend"
    if stuk.nr1 == eerste_stuk.nr1:
        return "prepend"


def is_valid_move_player(stuk: DominoStone, append: bool) -> bool:
    laatste_stuk = gamestate.snake[-1]
    eerste_stuk = gamestate.snake[0]


    if append:
        if stuk.nr1 == laatste_stuk.nr2:
            return True
        if stuk.nr2 == laatste_stuk.nr2:
            return True
    else:
        if stuk.nr2 == eerste_stuk.nr1:
            return True
        if stuk.nr1 == eerste_stuk.nr1:
            return True
    return False


def is_input_correct(my_input):
    try:
        my_input = int(my_input)
    except (ValueError, TypeError):
        return False

    try:

        gamestate.pieces[abs(my_input)-1]
    except IndexError:
        return False

    return True


def ask_player_input():
    while True:
        my_input = input()

        if not is_input_correct(my_input):
            print("Invalid input. Please try again.")
            continue
        my_input = int(my_input)
        if my_input == 0:
            return my_input

        stuk = gamestate.pieces[abs(my_input)-1]

        if not is_valid_move_player(stuk, append=my_input>0):
            print("Illegal move. Please try again.")
            continue
        return my_input


def ask_computer_input():
   input()
   is_valid_for_comp()


def is_game_gedaan():
    if len(gamestate.pieces_computer) and len(gamestate.pieces_player) == 0:
        print("Status: The game is over. It's a draw!")
    elif len(gamestate.pieces_computer) == 0:
        print("\nStatus: The game is over. The computer won!")
    elif len(gamestate.pieces_player) == 0:
        print("\nStatus: The game is over. You won!")
    else:
        return False

    return True


def wiens_beurt():
    if gamestate.player == "computer":
        print("\nStatus: Computer is about to make a move. Press Enter to continue...")
    if gamestate.player == "player":
        print("\nStatus: It's your turn to make a move. Enter your command.")


def print_dominosnake():
    geen_haakjes = str(gamestate.snake)[1:-1]
    geen_komma = geen_haakjes.replace(", [", "[")
    if len(gamestate.snake) < 6:
        print(geen_komma)
    else:
        print(f'{geen_komma[:17]}...{geen_komma[-17:]}')


def print_field():
    print("=" * 70)
    print(f'Stock size: {len(gamestate.pieces_hoop)}')
    if gamestate.player == "player":
        print(f'Computer pieces: {len(gamestate.pieces_computer)} \n')
    else:
        print(f'Computer pieces: {len(gamestate.pieces_computer)} \n')
    print_dominosnake()
    print("\nYour pieces:")
    for i, piece in enumerate(gamestate.pieces):
        print(f"{i+1}:{piece}")


def shuffle_deck() -> Tuple:
    """
    Shuffles the stones and returns the pieces for:
    - computer
    - player
    - stock
    """
    lijst = [
        DominoStone(x, y)
        for x, y in combinations_with_replacement(range(7), 2)
    ]
    random.shuffle(lijst)

    computer_pieces = lijst[:7]
    player_pieces = lijst[7:14]
    stock_pieces = lijst[14:]

    return computer_pieces, player_pieces, stock_pieces


def find_highest(deck: Sequence[DominoStone]) -> DominoStone:
    return sorted(deck)[-1]


def wie_begint(computer_pieces, player_pieces):
    sorted_computer = sorted([x for x in computer_pieces if x.is_double()], reverse=True)
    sorted_player = sorted([x for x in player_pieces if x.is_double()], reverse=True)

    double_computer = next(iter(sorted_computer), None)
    double_player = next(iter(sorted_player), None)

    if double_computer is None and double_player is None:
        raise NoDoubles

    if double_computer is None:
        return "player", double_player

    if double_player is None:
        return "computer", double_computer

    if double_computer > double_player:
        return "computer", double_computer

    return "player", double_player


def game_startup_phase():
    while True:
        gamestate.pieces_computer, gamestate.pieces_player, gamestate.pieces_hoop = (
            shuffle_deck()
        )

        try:
            gamestate.player, beginnend_stuk = wie_begint(gamestate.pieces_computer, gamestate.pieces_player)
            break
        except NoDoubles:
            pass

    return beginnend_stuk


def main():
    stuk = game_startup_phase()
    gamestate.play_piece(stuk)
    while True:
        print_field()
        if is_game_gedaan():
            break
        wiens_beurt()

        if gamestate.player == "player":
            my_input = ask_player_input()
            if my_input == 0:
                gamestate.take_piece()
                continue

            stuk = gamestate.pieces_player[abs(my_input)-1]
            gamestate.play_piece(stuk, append=my_input > 0)

        else:
            ask_computer_input()


if __name__ == '__main__':
    # player first move: 0
    # computer first move: 4
    random.seed(4)
    main()

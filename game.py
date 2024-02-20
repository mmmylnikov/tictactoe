"""
Ваше задние на эту неделю – написать консольную игру в крестики-нолики.

Поле 3х3, пользователь вводит координаты своего хода,
компьютер делает случайный ход,
кто играет крестиками выбирается случайно,
если кто-то выиграл – это выводится на экран.
"""

import random
from enum import Enum


class HeroAlias(Enum):
    TIC = "_X_"
    TAC = "_O_"
    TICTOE = "ХХХ"
    TACTOE = "OOO"
    BLANK = "___"


class Player:
    name: str
    is_pc: bool
    hero: HeroAlias = HeroAlias.BLANK

    def __init__(self, name: str | None = None, is_pc: bool = True) -> None:
        if not name:
            name = 'PC' if is_pc else 'User'
        self.name = name
        self.is_pc = is_pc

    def __str__(self) -> str:
        return f'{self.name} -> {self.hero.value}'

    def move_pc(
            self, possible_moves: list[tuple[int, int]]) -> tuple[int, int]:
        return random.choice(possible_moves)

    def move_user(
            self, possible_moves: list[tuple[int, int]]) -> tuple[int, int]:

        while True:
            coord_raw = input('Введите координаты хода: ')
            try:
                if coord_raw.strip().lower() == 'exit':
                    exit()
                x, y = coord_raw.strip().split(' ')
                coord = (int(x), int(y))
                if coord not in possible_moves:
                    raise ValueError()
            except ValueError:
                message = '!!! Такой ход недоступен, '
                message += 'введите координаты хода в формате "x y". '
                message += 'Для выхода введите "exit".'
                print(message)
                continue
            else:
                break
        return coord

    def move(self, possible_moves: list[tuple[int, int]]) -> tuple[int, int]:
        if self.is_pc:
            coord = self.move_pc(possible_moves=possible_moves)
        else:
            coord = self.move_user(possible_moves=possible_moves)
        print(f'Сделан ход -> "{coord[0]} {coord[1]}"')
        return coord


class Board:
    grid: list
    possible_moves: list[tuple[int, int]]
    blank_symbol = bs = HeroAlias.BLANK.value
    winning_lines: tuple

    def __init__(self) -> None:
        self.set_start_grid()
        self.set_start_possible_moves()
        self.set_winning_lines()

    def set_start_grid(self) -> None:
        self.grid = [
            [self.bs, self.bs, self.bs],
            [self.bs, self.bs, self.bs],
            [self.bs, self.bs, self.bs],
        ]

    def set_start_possible_moves(self) -> None:
        self.possible_moves = list()
        for row_id, row in enumerate(self.grid):
            for col_id, col in enumerate(row):
                self.possible_moves.append((row_id, col_id))

    def set_winning_lines(self) -> None:
        self.winning_lines = (
            # vertical lines
            ((0, 0), (0, 1), (0, 2)),
            ((1, 0), (1, 1), (1, 2)),
            ((2, 0), (2, 1), (2, 2)),
            # horizontal lines
            ((0, 0), (1, 0), (2, 0)),
            ((0, 1), (1, 1), (2, 1)),
            ((0, 2), (1, 2), (2, 2)),
            # diagonal lines
            ((0, 0), (1, 1), (2, 2)),
            ((0, 2), (1, 1), (2, 0)),
        )

    def print_possible_moves(self) -> None:
        print(f'Доступные ходы: ({len(self.possible_moves)})')
        print('; '.join([f'{x} {y}' for x, y in self.possible_moves]))

    def move(self, coord: tuple[int, int], player: Player) -> None:
        self.possible_moves.remove(coord)
        self.grid[coord[0]][coord[1]] = player.hero.value

    def check_winnings(self) -> list[HeroAlias] | None:
        for line_id, line in enumerate(self.winning_lines):
            row = [self.grid[cell[0]][cell[1]] for cell in line]
            row_set = set(row)
            if all([
                    len(row_set) == 1,
                    next(iter(row_set)) != HeroAlias.BLANK.value,
                    ]):
                self.possible_moves = []
                HERO_MAP = {
                        HeroAlias.TAC: HeroAlias.TACTOE,
                        HeroAlias.TIC: HeroAlias.TICTOE,
                    }
                current_hero = HeroAlias(next(iter(row_set)))
                current_hero_toe = HERO_MAP[current_hero]
                for cell in line:
                    self.grid[cell[0]][cell[1]] = current_hero_toe.value
                return [current_hero]
        if len(self.possible_moves) == 0:
            return [HeroAlias.TIC, HeroAlias.TAC]
        return None

    def draw(self, win: bool = False) -> None:
        print('Сейчас доска выглядит так:')
        print(' | '.join(['X\\Y']+[
            f'_{i}_' for i in range(len(self.grid[0]))
            ]))
        for row_id, row in enumerate(self.grid):
            print(' | '.join([f'_{row_id}_']+row))
        if not win:
            self.print_possible_moves()


class Game:
    board: Board
    whose_turn: Player
    players: list[Player]

    def __init__(self, board: Board, players: list[Player]) -> None:
        self.board = board
        self.players = players

    def assign_hero_to_players(self) -> None:
        hero_1 = random.choice([HeroAlias.TIC, HeroAlias.TAC])
        hero_2 = HeroAlias.TAC if hero_1 == HeroAlias.TIC else HeroAlias.TIC
        self.players[0].hero = hero_1
        self.players[1].hero = hero_2

        if hero_1 == HeroAlias.TIC:
            self.whose_turn = self.players[0]
        else:
            self.whose_turn = self.players[1]

        print('Список игроков:')
        for player in self.players:
            print(f' > {player}')

    def move(self) -> None:
        self.board.draw()
        current_player = self.whose_turn
        print(f'Сейчас ходит: {current_player}')
        coord = current_player.move(possible_moves=self.board.possible_moves)
        self.board.move(coord=coord, player=current_player)
        winners = self.board.check_winnings()
        if winners:
            print('=========================')
            self.board.draw(win=True)
            print('=========================')
            if len(winners) > 1:
                print('Победила дружба!')
            else:
                print(f'Победил: {current_player}')

        if current_player == self.players[0]:
            self.whose_turn = self.players[1]
        else:
            self.whose_turn = self.players[0]

        print('=========================')

    def run(self) -> None:
        self.assign_hero_to_players()
        while self.board.possible_moves:
            self.move()


def main() -> None:
    players = [
        Player(name='Max', is_pc=False),
        Player(name='PC', is_pc=True),
    ]
    game = Game(board=Board(), players=players)
    game.run()


if __name__ == "__main__":
    main()

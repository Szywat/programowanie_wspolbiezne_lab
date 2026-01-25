import random

class SudokuGame:
    def __init__(self):
        self.base = 3
        self.side = self.base * self.base
        self.full_board = []
        self.board = []
        self.scores = [0, 0]
        self.turn = 0
        self.game_over = False
        self.winner = None

    def generate_board(self):
        def pattern(r, c): return (self.base * (r % self.base) + r // self.base + c) % self.side

        def shuffle(s): return random.sample(s, len(s))

        rBase = range(self.base)
        rows = [g * self.base + r for g in shuffle(rBase) for r in shuffle(rBase)]
        cols = [g * self.base + c for g in shuffle(rBase) for c in shuffle(rBase)]
        nums = shuffle(range(1, self.base * self.base + 1))

        self.full_board = [[nums[pattern(r, c)] for c in cols] for r in rows]
        self.board = [row[:] for row in self.full_board]

        squares = self.side * self.side
        empties = 10
        for p in random.sample(range(squares), empties):
            self.board[p // self.side][p % self.side] = 0

    def make_move(self, player_id, row, col, val):
        if self.turn != player_id or self.game_over:
            return False, "Nie twoja tura lub koniec gry"

        correct_val = self.full_board[row][col]
        is_correct = (val == correct_val)

        if is_correct:
            self.scores[player_id] += 1
            self.board[row][col] = val
        else:
            self.scores[player_id] -= 1

        self.turn = 1 if self.turn == 0 else 0
        self.check_game_over()

        return True, is_correct

    def check_game_over(self):
        is_full = all(cell != 0 for row in self.board for cell in row)
        if is_full:
            self.game_over = True

            score_p0 = self.scores[0]
            score_p1 = self.scores[1]

            if score_p0 > score_p1:
                self.winner = 0
            elif score_p1 > score_p0:
                self.winner = 1
            else:
                self.winner = -1
        return self.game_over

    def get_state(self):
        return {
            "full_board": self.full_board,
            "board": self.board,
            "scores": self.scores,
            "turn": self.turn,
            "game_over": self.game_over,
            "winner": self.winner
        }
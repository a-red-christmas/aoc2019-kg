# Arcade game
# There is no way to win the game reactively. The paddle moves too slowly. The game, however, is
# deterministic. The following code repeatedly plays the game learning with each round where to
# move the paddle for the next round

import time
import pathlib
import pickle
import sys
from collections import deque
from intcode import IntCodeComputer, ProgramState


class Game:
    def __init__(self):
        self.screen = {}
        self.score = 0

        # Internal state needed for learning
        self._baseline = 21

        self._ball_pos = 0
        self._ball_pos_at_miss = 0
        self._paddle_pos = 0
        self._paddle_pos_at_miss = 0

    def set_state(self, x, y, t):
        if x == -1 and y == 0:
            self.score = max(self.score, t)
        else:
            if t == 3:
                self._paddle_pos = x
            if t == 4:
                self._ball_pos = x
                if y == self._baseline:
                    self._ball_pos_at_miss = x
                    self._paddle_pos_at_miss = self._paddle_pos

            self.screen[(x, y)] = t

    def current_paddle_gap(self):
        return self._ball_pos - self._paddle_pos

    def paddle_gap_at_miss(self):
        return self._ball_pos_at_miss - self._paddle_pos_at_miss

    def balls_left(self):
        return sum(1 for v in self.screen.values() if v == 2)

    def draw(self):
        print(f"s={self.score} b={self.balls_left()}")
        self.print_screen()

    def print_screen(self):
        extent = (
            min(p[0] for p in self.screen.keys()),
            min(p[1] for p in self.screen.keys()),
            max(p[0] for p in self.screen.keys()),
            max(p[1] for p in self.screen.keys())
        )

        legend = {
            0: " ",
            1: "#",
            2: "*",
            3: "_",
            4: "o"
        }

        for j in range(extent[1], extent[3] + 1):
            print("".join(legend[self.screen.get((i, j), 0)] for i in range(extent[0], extent[2] + 1)))


class ArcadeBox:
    def __init__(self, core, debug=False):
        self.game = Game()
        self.computer = IntCodeComputer(debug=debug)
        self.computer.load_core(core)
        self.computer.state = ProgramState.running

    def play_step(self, joy):
        self.computer.input_buffer = [joy]
        while len(self.computer.input_buffer) and self.computer.state == ProgramState.running:
            self.computer.step()
            if len(self.computer.output_buffer) == 3:
                x, y, t = self.computer.output_buffer
                self.computer.output_buffer.clear()
                self.game.set_state(x, y, t)

    def display(self):
        self.game.draw()


def printable_moves(moves):
    _m = {
        0: "-",
        1: "R",
        -1: "L"
    }
    return "".join(_m[m] for m in moves)


def move_atoi(initial_moves):
    _m = {
        "-": 0,
        "L": -1,
        "R": 1
    }
    return [_m[m] for m in initial_moves]


class Debugger:
    def __init__(self, cols=20, rows=20):
        self.cols, self.rows = cols, rows
        self.box = None

    def step(self, computer: IntCodeComputer):
        print(f"sc={self.box.game.score} balls={self.box.game.balls_left()}")
        print(f"pc={computer.program_counter}")
        for i in range(self.rows):
            print("".join(
                f" {computer._core[self.cols * i + j]:#6}" for j in range(self.cols) if self.cols * i + j < len(
                    computer._core)))
        time.sleep(0.01)


def print_core(new_core, old_core):
    for i in range(len(old_core)):
        if old_core[i] != new_core[i]:
            print(f"{i}: {old_core[i]} -> {new_core[i]}")


def main():
    with open("013.1.input.txt", "r") as f:
        core = [int(c) for c in f.readline().strip().split(",")]

    core[0] = 2  # Set mode to play for free
    initial_moves = move_atoi(open("013.2.moves-checkpoint2.txt", "r").readline().strip())
    mv_no = 0

    box = ArcadeBox(core)

    last_score = 0

    score_locs = []

    while box.computer.state == ProgramState.running and mv_no < len(initial_moves):
        joy = initial_moves[mv_no]
        box.play_step(joy)
        if box.game.score > last_score:
            # print(f"balls={box.game.balls_left()} score={box.game.score}")
            # print(f"{box.computer._core[435]}, {box.game.score}")
            sl = box.computer._core[435]
            score_locs += [(sl, box.computer._core[sl], box.game.score - last_score)]
            # print(score_locs[-1])

            last_score = box.game.score
        mv_no += 1

    # print("\n".join(box.computer.get_log()))

    screen = {}
    for l in score_locs:
        _n = l[0] - 1651
        # l = row * 44 + col
        col = _n % 44
        row = _n // 44
        screen[(row, col)] = 1

    for row in range(23):
        print("".join("X" if screen.get((row, col)) else " " for col in range(44)))


main()

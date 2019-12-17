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
    def __init__(self, core):
        self.game = Game()
        self.computer = IntCodeComputer()
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


class Learner:
    def __init__(self):
        self.paddle_gap_at_end = 0
        self.moves_played = []

    def learn(self, box, moves_played):
        if box.game.balls_left() == 0:
            return moves_played

        paddle_gap_at_end = box.game.paddle_gap_at_miss()

        if moves_played[-1] != 0:
            # Our mysterious off by one error
            sign = 1 if self.paddle_gap_at_end >= 0 else -1
            streak = sign * (abs(self.paddle_gap_at_end) + 1)
        else:
            streak = paddle_gap_at_end

        if paddle_gap_at_end > 0:
            moves_played[-abs(streak):] = [1] * streak

        if paddle_gap_at_end < 0:
            moves_played[-abs(streak):] = [-1] * -streak

        self.moves_played = moves_played
        self.paddle_gap_at_end = streak

        return moves_played


class RobotPlayer:

    cache_file = pathlib.Path("013.2.cache.pkl")

    def __init__(self, game_core, use_core_cache=False):
        self.joystick = []
        self.learner = Learner()
        self.game_core = game_core
        self.use_core_cache = use_core_cache

    def load_from_cache(self):
        if self.cache_file.exists():
            cache = pickle.load(self.cache_file.open("rb"))
        else:
            return None

        if cache.get("original_core") == self.game_core:
            mp = cache.get("moves_played")
            if mp == self.joystick[:len(mp)]:
                return cache

    def save_core_cache(self, box, moves_played):
        cache = {
            "original_core": self.game_core,
            "arcadebox": box,
            "moves_played": moves_played
        }
        pickle.dump(cache, self.cache_file.open("wb"))

    def play_round(self, display_last=0):
        cache = self.load_from_cache()
        if cache is not None and self.use_core_cache:
            box = cache.get("arcadebox")
            moves_played = cache.get("moves_played")
            proposed_moves = deque(self.joystick[len(moves_played):])
        else:
            box = ArcadeBox(self.game_core)
            moves_played = []
            proposed_moves = deque(self.joystick)

        while box.computer.state == ProgramState.running:
            if len(proposed_moves) == 50:  # Don't make this too small ...
                self.save_core_cache(box, moves_played)

            joy = proposed_moves.popleft() if proposed_moves else 0

            moves_played += [joy]
            box.play_step(joy)
            print(chr(27) + "[2J")
            print(printable_moves(moves_played)[-44:])
            print(f"balls={box.game.balls_left()} score={box.game.score}")
            box.display()
            time.sleep(.05)

        # Discard last move
        moves_played = moves_played[:-1]
        self.joystick = self.learner.learn(box, moves_played)

        print(chr(27) + "[2J")
        print(f"miss={box.game.paddle_gap_at_miss()}")
        print(f"balls={box.game.balls_left()} score={box.game.score}")
        box.display()
        time.sleep(1)

        return box.game.balls_left()

    def play_to_win(self, initial_moves=None, display_last=0):
        if initial_moves is not None:
            _m = {
                "-": 0,
                "L": -1,
                "R": 1
            }
            self.joystick = [_m[m] for m in initial_moves]

        while self.play_round(display_last):
            with open("013.2.moves.txt", "w") as f:
                f.write(printable_moves(self.joystick))


def main():
    with open("013.1.input.txt", "r") as f:
        core = [int(c) for c in f.readline().strip().split(",")]

    core[0] = 2  # Set mode to play for free
    initial_moves = open("013.2.moves.txt", "r").readline().strip()
    # initial_moves = open("013.2.moves-checkpoint1.txt", "r").readline().strip()
    # initial_moves = None
    player = RobotPlayer(core, use_core_cache=True)
    player.play_to_win(initial_moves, display_last=5)


main()

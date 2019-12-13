# Arcade game
# There is no way to win the game reactively. The paddle moves too slowly. The game, however, is
# deterministic. The following code repeatedly plays the game learning with each round where to
# move the paddle for the next round

import time
import sys
from collections import deque
from intcode import IntCodeComputer, ProgramState


class Game:
    def __init__(self):
        self.screen = {}
        self.score = 0

        # Internal state needed for learning
        self._baseline = 21

        self._ball_pos_at_miss = 0
        self._paddle_pos = 0
        self._paddle_pos_at_miss = 0

    def set_state(self, x, y, t):
        if x == -1 and y == 0:
            self.score = max(self.score, t)
        else:
            if t == 3:
                self._paddle_pos = x
            if t == 4 and y == self._baseline:
                self._ball_pos_at_miss = x
                self._paddle_pos_at_miss = self._paddle_pos

            self.screen[(x, y)] = t

    def paddle_gap(self):
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


class RobotPlayer:
    def __init__(self, game_core):
        self.joystick = []
        self.game_core = game_core
        self.current_box = None

    def play_round(self, full_display=False):
        box = ArcadeBox(self.game_core)
        moves_played = []
        proposed_moves = deque(self.joystick)

        while box.computer.state == ProgramState.running:
            joy = proposed_moves.popleft() if proposed_moves else 0
            moves_played += [joy]
            box.play_step(joy)
            if full_display:
                print(printable_moves(moves_played)[-80:])
                print(box.game.paddle_gap())
                box.display()
                time.sleep(.2)

        # Discard last move
        moves_played = moves_played[:-1]
        self.joystick = predicted_moves(box, moves_played)

        self.current_box = box
        return box.game.balls_left()

    def play_to_win(self, initial_moves=None, full_display=False):
        if initial_moves is not None:
            _m = {
                "-": 0,
                "L": -1,
                "R": 1
            }
            self.joystick = [_m[m] for m in initial_moves]

        while self.play_round(full_display):
            with open("013.2.moves.txt", "w") as f:
                f.write(printable_moves(self.joystick))

            if full_display:
                time.sleep(1)
            else:
                print(f"s={self.current_box.game.score} b={self.current_box.game.balls_left()}")


def predicted_moves(box, moves_played):
    if box.game.balls_left() == 0:
        return moves_played

    paddle_gap_at_end = box.game.paddle_gap()

    if moves_played[-1] != 0:
        raise RuntimeError("Un-winnable game!")

    if paddle_gap_at_end > 0:
        #paddle_gap_at_end += 1
        moves_played[-abs(paddle_gap_at_end):] = [1] * paddle_gap_at_end

    if paddle_gap_at_end < 0:
        #paddle_gap_at_end -= 1
        moves_played[-abs(paddle_gap_at_end):] = [-1] * -paddle_gap_at_end

    return moves_played


def main():
    with open(sys.argv[1], "r") as f:
        core = [int(c) for c in f.readline().strip().split(",")]

    core[0] = 2  # Set mode to play for free
    initial_moves = open("013.2.moves.txt", "r").readline().strip()
    player = RobotPlayer(core)
    #player.play_round()
    player.play_to_win(initial_moves)


main()

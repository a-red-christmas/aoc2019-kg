# Arcade game
# Unabashed cheating by altering the core while the game is running
# Create a paddle that extends the whole width of the screen

import time
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
    def __init__(self, core, core_hacker_func):
        self.game = Game()
        self.computer = IntCodeComputer()
        self.computer.load_core(core)
        self.computer.state = ProgramState.running

        self.core_hacker_func = core_hacker_func

    def play_step(self, joy):
        self.computer.input_buffer = [joy]
        while len(self.computer.input_buffer) and self.computer.state == ProgramState.running:
            self.computer.step()
            self.core_hacker_func(self.computer)
            if len(self.computer.output_buffer) == 3:
                x, y, t = self.computer.output_buffer
                self.computer.output_buffer.clear()
                self.game.set_state(x, y, t)

    def display(self):
        self.game.draw()


def infinite_paddle(computer):
    computer._core[639 + 21*44 + 1:639 + 21*44 + 43] = [3] * 42


def main():
    with open("013.1.input.txt", "r") as f:
        core = [int(c) for c in f.readline().strip().split(",")]

    core[0] = 2  # Set mode to play for free
    box = ArcadeBox(core, infinite_paddle)

    last_score = 0
    while box.computer.state == ProgramState.running:
        box.play_step(0)
        print(chr(27) + "[2J")
        print(f"balls={box.game.balls_left()} score={box.game.score}")
        box.display()
        time.sleep(.05)


main()

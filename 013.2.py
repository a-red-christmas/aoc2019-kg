# Arcade game
# There is no way to win the game reactively. The paddle moves too slowly. The game, however, is
# deterministic. The following code repeatedly plays the game learning with each round where to
# move the paddle for the next round

import sys
from collections import deque
from intcode import IntCodeComputer, ProgramState


class GameState:
    def __init__(self):
        self.screen = {}
        self.score = None

        # Internal state needed for learning
        self._baseline = 21

        self._ball_pos = (0, 0)
        self._paddle_pos = (0, 0)

    def set_state(self, x, y, t):
        if x == -1 and y == 0:
            self.score = t
        else:
            if t == 3:
                self._paddle_pos = (x, y)
                # y == baseline
            if t == 4 and y == self._baseline:
                self._ball_pos = (x, y)

            self.screen[(x, y)] = t

    def paddle_gap(self):
        return self._ball_pos[0] - self._paddle_pos[0]

    def balls_left(self):
        return sum(1 for v in self.screen.values() if v == 2)

    def draw(self):
        print(f"s={self.score} b={self._ball_pos} p={self._paddle_pos}")
        print_screen(self.screen)


class GameResult:
    def __init__(self):
        self.score = 0
        self.balls_left = 0
        self.joystick = []
        self.paddle_gap_at_end = 0
        self.game_state = None

    def predicted_joy_commands(self):
        if self.joystick[-abs(self.paddle_gap_at_end)] != 0:
            raise RuntimeError("Un-winnable game!")

        if self.paddle_gap_at_end > 0:
            self.joystick[-abs(self.paddle_gap_at_end):] = [1] * self.paddle_gap_at_end

        if self.paddle_gap_at_end < 0:
            self.joystick[-abs(self.paddle_gap_at_end):] = [-1] * -self.paddle_gap_at_end

        return self.joystick

    def __str__(self):
        return f"s={self.score} b={self.balls_left}"


def play_game(core, _joystick):

    joystick = deque(_joystick)

    game = GameState()
    computer = IntCodeComputer()
    computer.load_core(core)
    computer.state = ProgramState.running

    gr = GameResult()
    while computer.state == ProgramState.running:
        computer.step()

        if len(computer.output_buffer) == 3:
            x, y, t = computer.output_buffer
            computer.output_buffer.clear()
            game.set_state(x, y, t)

        if len(computer.input_buffer) == 0 and len(game.screen):
            game.draw()
            if joystick:
                joy = joystick.popleft()
            else:
                joy = 0

            gr.joystick += [joy]
            computer.input_buffer = [joy]

    # game.draw()
    gr.balls_left = game.balls_left()
    gr.paddle_gap_at_end = game.paddle_gap()
    gr.game_state = game
    return gr


def learn_game(core):
    bl = 100000
    joystick = []
    while bl:
        gr = play_game(core, joystick)
        print(gr, joystick)
        joystick = gr.predicted_joy_commands()


def main():
    with open(sys.argv[1], "r") as f:
        core = [int(c) for c in f.readline().strip().split(",")]

    core[0] = 2  # Set mode to play for free
    learn_game(core)


def print_screen(screen):
    extent = (
        min(p[0] for p in screen.keys()),
        min(p[1] for p in screen.keys()),
        max(p[0] for p in screen.keys()),
        max(p[1] for p in screen.keys())
    )

    legend = {
        0: " ",
        1: "#",
        2: "*",
        3: "_",
        4: "o"
    }

    for j in range(extent[1], extent[3] + 1):
        print("".join(legend[screen.get((i, j), 0)] for i in range(extent[0], extent[2] + 1)))


main()

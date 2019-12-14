# Arcade game
import sys
from intcode import IntCodeComputer, ProgramState


def main():
    with open(sys.argv[1], "r") as f:
        core = [int(c) for c in f.readline().strip().split(",")]

    screen = {}

    computer = IntCodeComputer()
    computer.load_core(core)
    computer.state = ProgramState.running
    while computer.state == ProgramState.running:
        computer.step()

        if len(computer.output_buffer) == 3:
            x, y, t = computer.output_buffer
            computer.output_buffer.clear()
            screen[(x, y)] = t

    print(len([s for s in screen.values() if s == 2]))
    print_screen(screen)


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

    for j in range(extent[3], extent[1] - 1, -1):
        print("".join(legend[screen.get((i, j), 0)] for i in range(extent[0], extent[2] + 1)))


main()

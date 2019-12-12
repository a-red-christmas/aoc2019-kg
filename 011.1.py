import sys
from intcode import IntCodeComputer, ProgramState


class PaintingRobot:

    turn_right = {
        (0, 1): (1, 0),
        (1, 0): (0, -1),
        (0, -1): (-1, 0),
        (-1, 0): (0, 1)
    }

    turn_left = {
        (0, 1): (-1, 0),
        (-1, 0): (0, -1),
        (0, -1): (1, 0),
        (1, 0): (0, 1)
    }

    def __init__(self):
        self.pos = (0, 0)
        self.dir = (0, 1)
        self._painted_panels = set()

    def camera(self, panel):
        return panel.get(self.pos, 0)

    def paint(self, color, panel):
        panel[self.pos] = color
        self._painted_panels.add(self.pos)

    def turn(self, _dir):
        self.dir = self.turn_left[self.dir] if _dir == 0 else self.turn_right[self.dir]
        self.pos = (self.pos[0] + self.dir[0], self.pos[1] + self.dir[1])


def print_panel(panel, extent):
    for j in range(extent[3], extent[1] - 1, -1):
        print("".join("." if panel.get((i, j), 0) == 0 else "#" for i in range(extent[0], extent[2] + 1)))


def test_robots():
    instructions = [(1, 0), (0, 0), (1, 0), (1, 0), (0, 1), (1, 0), (1, 0)]
    panel = {}
    pr = PaintingRobot()
    for inst in instructions:
        pr.paint(inst[0], panel)
        pr.turn(inst[1])
        print()
        print_panel(panel, [-2, -2, 2, 2])

    print(len(pr._painted_panels))


def run_robot_run(core):

    panel = {}
    pr = PaintingRobot()

    computer = IntCodeComputer()
    computer.load_core(core)
    computer.state = ProgramState.running
    while computer.state == ProgramState.running:
        computer.set_input_buffer([pr.camera(panel)])

        inst = [None, None]
        while len(computer.output_buffer) == 0:
            computer.step()
            if computer.state != ProgramState.running:
                return len(pr._painted_panels)

        inst[0] = computer.output_buffer.pop()

        while len(computer.output_buffer) == 0:
            computer.step()
        inst[1] = computer.output_buffer.pop()

        pr.paint(inst[0], panel)
        pr.turn(inst[1])


def main():
    with open(sys.argv[1], "r") as f:
        core = [int(c) for c in f.readline().strip().split(",")]
    print(run_robot_run(core))


# test_robots()
main()

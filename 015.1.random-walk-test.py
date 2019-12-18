# Just let robot do a random walk and see what happens ...
# If no obstacle keep moving in the same direction
# If obstacle, try turning right. If we've been here before, turn right again
# If all else fails. Go back the way we came

from collections import deque
import time
from intcode import IntCodeComputer, ProgramState


# IntCode move code re direction
news = {
    1: (0, 1),  # N
    2: (0, -1), # S
    3: (-1, 0), # W
    4: (1, 0)   # E
}

turn_right = {
    1: 4,
    2: 3,
    3: 1,
    4: 2
}


def new_loc(loc, move):
    m = news[move]
    return loc[0] + m[0], loc[1] + m[1]


class Droid:
    def __init__(self, core, loc):
        self.computer = IntCodeComputer()
        self.computer.load_core(core)
        self.computer.state = ProgramState.running
        self.loc = loc
        self.heading = 4
        self.grid_map = {self.loc: 1}
        # self.headings = list(next_heading[self.heading])

    def move(self):
        self.heading = self.get_next_heading()
        self.computer.set_input_buffer([self.heading])
        while len(self.computer.output_buffer) == 0:
            self.computer.step()
        res = self.computer.output_buffer.pop()

        if res != 0:
            self.loc = new_loc(self.loc, self.heading)
            if res == 2:
                self.grid_map[self.loc] = -2 # Oxygen
            else:
                self.grid_map[self.loc] = self.grid_map.get(self.loc, 0) + 1 # visited
        else:
            self.grid_map[new_loc(self.loc, self.heading)] = -1  # block

        return res

    def get_next_heading(self):
        new_heading = self.heading

        # Find an uncharted way
        for n in [0, 1, 2, 3]:
            _loc = new_loc(self.loc, new_heading)
            if _loc not in self.grid_map:
                return new_heading
            else:
                new_heading = turn_right[new_heading]

        # Find a free way that we have traveled least
        new_heading = self.heading
        min_trips, min_heading = 10000, new_heading
        for n in [0, 1, 2, 3]:
            _loc = new_loc(self.loc, new_heading)
            if self.grid_map[_loc] != -1:
                if self.grid_map[_loc] < min_trips:
                    min_trips = self.grid_map[_loc]
                    min_heading = new_heading
            new_heading = turn_right[new_heading]

        return min_heading

    def display_map(self):
        legend = {
            -2: "$",
            -1: "#",
            1: ".",
            0: " "
        }
        extent = [-20, -30, 30, 30]
        print(chr(27) + "[2J")
        print(f"h={self.heading}")
        for col in range(extent[0], extent[2]):
            print("".join("*" if (row, col) == self.loc else legend[min(self.grid_map.get((row, col), 0), 1)]
                          for row in range(extent[1], extent[3])))
        time.sleep(.1)


def main():
    with open("015.1.input.txt", "r") as f:
        core = [int(c) for c in f.readline().strip().split(",")]

    droid = Droid(core, loc=(0, 0))
    for n in range(10000):
        r = droid.move()
        droid.display_map()
        if r == 2:
            break


def print_ship_map(ship_map, droid):
    # extent = [
    #     min(p[0] for p in ship_map.keys()),
    #     min(p[1] for p in ship_map.keys()),
    #     max(p[0] for p in ship_map.keys()),
    #     max(p[1] for p in ship_map.keys())
    # ]
    extent = [-20, -40, 20, 40]
    print(chr(27) + "[2J")
    print(f"h={droid.heading}")
    for col in range(extent[0], extent[2]):
        print("".join("*" if (row, col) == droid.loc else ("." if (row, col) in ship_map else "#")
                      for row in range(extent[1], extent[3])))
    time.sleep(.1)


main()

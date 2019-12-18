# If we were given the whole map, we could do a breadth first
# search and end up with the shortest number of steps.
#
# We are however, given a stateful system. One (expensive)
# way could be to copy the computer state over for each search
# candidate and perform a breadth first search that way. The problem
# is that we are likely to run out of memory (depending on how
# far the oxygen system is and how few obstacles there are). We
# are likely to end up with N copies of the memory where N is the
# search depth (roughly, as many copies as the circumference of the
# circle of radius N).
#
# We could reduce this by using a memory diff system where we compute
# and pass around memory diffs and only use one complete copy of the
# core for each robot run. This is worth a look.
#
# If we follow the idea that we have only one physical robot
# we could attempt a spiral each pattern for mapping, followed by
# a BFS on the resultant map.
#
# Let's try with a BFS method that clones the Droid computer at each
# step. The core is 3KB - we can afford to have a few copies floating
# around
#

import time
from collections import deque
from intcode import IntCodeComputer, ProgramState


news = {
    1: (0, 1),
    2: (0, -1),
    3: (-1, 0),
    4: (1, 0)
}


def new_loc(loc, move):
    m = news[move]
    return loc[0] + m[0], loc[1] + m[1]


class Droid:
    def __init__(self, computer, loc, depth):
        self.computer = computer
        self.loc = loc
        self.depth = depth

    def clone_and_move(self, move):
        new_droid = Droid(self.computer.clone(), new_loc(self.loc, move), self.depth + 1)
        new_droid.computer.set_input_buffer([move])
        while len(new_droid.computer.output_buffer) == 0:
            new_droid.computer.step()
        res = new_droid.computer.output_buffer.pop()
        return res, new_droid


all_moves = [1, 2, 3, 4]


def new_locs(loc, depth):
    return [(new_loc(loc, m), depth) for m in all_moves]


def main():
    with open("015.1.input.txt", "r") as f:
        core = [int(c) for c in f.readline().strip().split(",")]

    visited = {(0, 0)}
    computer = IntCodeComputer()
    computer.load_core(core)
    computer.state = ProgramState.running
    search_q = deque([Droid(computer, loc=(0, 0), depth=0)])

    while search_q:
        droid = search_q.popleft()
        for move in all_moves:
            res, new_droid = droid.clone_and_move(move)
            if res == 0:
                visited.add(new_droid.loc)
                continue
            elif res == 1:
                if new_droid.loc in visited:
                    continue
                else:
                    search_q.append(new_droid)
                    visited.add(new_droid.loc)
            elif res == 2:
                print(new_droid.depth)
                return 0

        display_visited(visited)
        time.sleep(.1)


def display_visited(visited):
    extent = [-20, -30, 30, 30]
    print(chr(27) + "[2J")
    for col in range(extent[0], extent[2]):
        print("".join("*" if (row, col) in visited else " " for row in range(extent[1], extent[3])))


main()

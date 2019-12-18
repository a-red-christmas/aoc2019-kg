# We use the BFS method developed earlier and doe a full search to map the area fully
# We then take this map and do a second BFS search, starting with the oxygen location
# and figure out the depth (time) it takes to fill the map

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


def create_map():
    with open("015.1.input.txt", "r") as f:
        core = [int(c) for c in f.readline().strip().split(",")]

    # 1 = block
    # 2 = corridor

    visited = {(0, 0): 2}
    computer = IntCodeComputer()
    computer.load_core(core)
    computer.state = ProgramState.running
    search_q = deque([Droid(computer, loc=(0, 0), depth=0)])

    oxy_source = None

    while search_q:
        droid = search_q.popleft()
        for move in all_moves:
            loc2 = new_loc(droid.loc, move)
            if loc2 in visited:
                continue

            res, new_droid = droid.clone_and_move(move)
            if res == 0:
                visited[new_droid.loc] = 1
                continue
            else:
                search_q.append(new_droid)
                visited[new_droid.loc] = 2
                if res == 2:
                    oxy_source = new_droid.loc

        display_visited(visited)
        print(f"Mapping: depth={droid.depth} clones={len(search_q)}")
        time.sleep(.01)

    return visited, oxy_source


def display_visited(visited):
    legend = [" ", "#", ".", "X", "$"]
    extent = [-20, -30, 30, 30]
    print(chr(27) + "[2J")
    for col in range(extent[0], extent[2]):
        print("".join(legend[visited.get((row, col), 0)] for row in range(extent[1], extent[3])))


def main():
    station_map, oxy_source = create_map()
    time.sleep(2)

    visited = {}
    d = 0
    search_q = deque([(oxy_source, d)])
    while search_q:
        loc, d = search_q.popleft()
        visited[loc] = 2
        for move in all_moves:
            loc2 = new_loc(loc, move)
            if loc2 in visited:
                continue
            if station_map.get(loc2) == 1:
                visited[loc2] = 1
                continue
            search_q.append((loc2, d + 1))

        display_visited(visited)
        print(f"Oxygenating: mins={d} tendrils={len(search_q)}")
        time.sleep(.1)


main()

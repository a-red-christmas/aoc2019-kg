# We pass as input the grid and the location of the laser base
# We then compute the x, y slopes of each asteroid.
# Put each asteroid in a bin indexed by normalized (x, y)
# The order in which the asteroid goes in the bin is from
# nearest to furthest
#
# We arrange these (x, y) pairs in quadrant order as follows
#
# Q1  (x >= 0, y >= 0) order descending by y/x
# Q2  (x >= 0, y < 0) order ascending by abs(y/x)
# Q3  (x < 0, y < 0) order descending by abs(y/x)
# Q4  (x < 0, y >= 0) order ascending by abs(y/x)

# Make 200 passes as follows
# Starting from the begining of the list, remove (x, y) pairs that are closest

import time
import sys
from collections import deque


class Grid(set):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extent = None


def main():
    grid = load_grid()
    p1 = (23, 20)
    sight_lines = sort_sight_lines(mark_sight_lines(p1, grid))

    # Debugging the sweep of the laser
    # for s in sight_lines:
    #     plot_sweeps(p1, [s], grid)

    p = None
    sl = 0
    ctr = 0
    while any(len(s) > 0 for s in sight_lines):
        if sight_lines[sl]:
            p = sight_lines[sl].popleft()
            ctr += 1
            print(ctr, p)
        sl = (sl + 1) % len(sight_lines)


def load_grid():
    grid = Grid()
    grid.extent = [None, None]
    with open(sys.argv[1], "r") as f:
        y = 0
        for line in f.readlines():
            line = line.strip()
            grid.extent[0] = len(line)
            for x, c in enumerate(line):
                if c == "#":
                    grid.add((x, y))
            y += 1
        grid.extent[1] = y
    return grid


def print_grid(grid):
    N, M = grid.extent
    for j in range(M):
        print("".join("#" if (i, j) in grid else "." for i in range(N)))


def mark_sight_lines(p1, grid):
    sight_lines = {}

    for p2 in grid:
        if p1 == p2:
            continue
        x, y = simplify_slope(p2[0] - p1[0], p2[1] - p1[1])
        if (x, y) in sight_lines:
            continue
        else:
            sight_lines[(x, y)] = mark(p1, x, y, grid)

    return sight_lines


def sort_sight_lines(sight_lines):
    keys = sight_lines.keys()
    slopes = [(k, abs(k[1] / (k[0] + 1e-9))) for k in keys]
    Q1 = sorted((s for s in slopes if s[0][0] >= 0 and s[0][1] <= 0), key=lambda x: x[1], reverse=True)
    Q2 = sorted((s for s in slopes if s[0][0] >= 0 and s[0][1] > 0), key=lambda x: x[1])
    Q3 = sorted((s for s in slopes if s[0][0] < 0 and s[0][1] > 0), key=lambda x: x[1], reverse=True)
    Q4 = sorted((s for s in slopes if s[0][0] < 0 and s[0][1] <= 0), key=lambda x: x[1])

    return [deque(sight_lines[q[0]]) for q in Q1 + Q2 + Q3 + Q4]


primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
max_no = primes[-1] ** 2


def simplify_slope(dx, dy):
    x, y = abs(dx), abs(dy)
    if x >= max_no or y >= max_no:
        raise RuntimeError("Prime list too small")

    while 1:
        for p in primes:
            if x % p == 0 and y % p == 0:
                x, y = x // p, y // p
                break
        else:
            return x if dx > 0 else -x, y if dy > 0 else -y


def mark(p1, dx, dy, grid):
    _x, _y = p1[0] + dx, p1[1] + dy
    x1, y1 = grid.extent

    q = []
    while 0 <= _x < x1 and 0 <= _y < y1:
        if (_x, _y) in grid:
            q.append((_x, _y))
        _x, _y = _x + dx, _y + dy

    return q


def plot_sweeps(p1, sight_lines, grid):
    for s in sight_lines:
        g = Grid(s)
        g.add(p1)
        g.extent = grid.extent
        print("-------")
        print_grid(g)
        time.sleep(.3)



main()

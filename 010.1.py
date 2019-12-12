# This is a classic problem.
# Due to time constraints, and after seeing the size of the input, I went
# with a straight forward O(n^2) solution. There are probably some tricks
# we could do to avoid duplicate work.

# O(n^2) algorithm
# For each of the n points (i)
# Consider all the other n - 1 points and compute the slope (x, y) for them
# For each slope reduce them to "normal form" which is (x', y')
# Where x' and y' are the smallest integers that maintain the fraction
# Now for k = [1, 2, ...] and k = [-1, -2, ...] test if there are any
# targets on (kx', ky'). The first target is visible and all subsequent
# ones are blocked. Mark all visited targets as done. We don't have
# to test them a second time.
# We search k to the extents of our grid (i.e. the min/max values of our
# target)

import sys


class Grid(set):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extent = None


def main():
    grid = load_grid()
    max_p, max_vis = max(((p1, compute_visible(p1, grid)) for p1 in grid), key=lambda x: x[1])
    print(max_p, max_vis)


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


def compute_visible(p1, grid):
    visible = set()
    invisible = set()

    for p2 in grid:
        if p1 == p2:
            continue

        if p2 in visible or p2 in invisible:
            continue
        x, y = simplify_slope(p2[0] - p1[0], p2[1] - p1[1])
        mark(p1, x, y, visible, invisible, grid)

    return len(visible)


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


def mark(p1, dx, dy, visible, invisible, grid):
    _x, _y = p1[0] + dx, p1[1] + dy
    x1, y1 = grid.extent
    nearest = True
    while 0 <= _x < x1 and 0 <= _y < y1:
        if (_x, _y) in grid:
            if nearest:
                visible.add((_x, _y))
                nearest = False
            else:
                invisible.add((_x, _y))

        _x, _y = _x + dx, _y + dy


main()

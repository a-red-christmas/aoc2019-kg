# Use a set to represent the panel
# In the first pass, mark all the cells in the panel that the
# first wire covers. In the second pass trace the second wire
# and when coming across an intersection, compute the distance,
# keep the closest one.

import sys


def main():
    with open(sys.argv[1]) as f:
        wires = [
            l.strip().split(",")
            for l in f.readlines()
        ]

    panel = set()
    place(wires[0], panel)
    d = closest_short_circuit(wires[1], panel)
    print(d)


def place(wire, panel):
    xy = (0, 0)
    for segment in wire:
        cell = xy
        for cell in trace(xy, segment):
            panel.add(cell)
        xy = cell


def closest_short_circuit(wire, panel):
    xy = (0, 0)
    min_d = None
    for segment in wire:
        cell = xy
        for cell in trace(xy, segment):
            if cell in panel:
                if min_d is None:
                    min_d = abs(cell[0]) + abs(cell[1])
                else:
                    min_d = min(min_d, abs(cell[0]) + abs(cell[1]))
        xy = cell

    return min_d


def trace(start, segment):
    dirn, dist = segment[0], int(segment[1:])

    if dirn == "R":
        return [
            (start[0] + i + 1, start[1])
            for i in range(dist)
        ]
    elif dirn == "L":
        return [
            (start[0] - i - 1, start[1])
            for i in range(dist)
        ]
    elif dirn == "U":
        return [
            (start[0], start[1] + i + 1)
            for i in range(dist)
        ]
    elif dirn == "D":
        return [
            (start[0], start[1] - i - 1)
            for i in range(dist)
        ]


if __name__ == "__main__":
    main()
# We use the same strategy as pt 1 but use a dict now, instead of a set
# and the values are the distances to that cell

import sys


def main():
    with open(sys.argv[1]) as f:
        wires = [
            l.strip().split(",")
            for l in f.readlines()
        ]

    panel = {}
    place(wires[0], panel)
    d = closest_short_circuit(wires[1], panel)
    print(d)


def place(wire, panel):
    xy, d = (0, 0), 0
    for segment in wire:
        cell = xy
        for cell in trace(xy, segment):
            d += 1
            panel[cell] = d
        xy = cell


def closest_short_circuit(wire, panel):
    xy, d = (0, 0), 0
    min_d = None
    for segment in wire:
        cell = xy
        for cell in trace(xy, segment):
            d += 1
            if cell in panel:
                if min_d is None:
                    min_d = panel[cell] + d
                else:
                    min_d = min(min_d, panel[cell] + d)
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
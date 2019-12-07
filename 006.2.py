# Here we are asked to find the first common ancestor of the two nodes
# We do this climbing up one target to the root, marking depths as we go
# We next climb up the other target, marking depths as we go. When we reach
# an already visited node, we know that is the first common ancestor and we sum
# the depths
# In this problem, we invert the representation: for each node, we mark the parent
# We also leave room in the implementation for a depth flag

import sys
from collections import deque


def make_tree_from_input(lines):
    tree = {}
    for line in lines:
        center, satellite = line.strip().split(")")
        tree[satellite] = [center, None]
    return tree


def transfer_distance(orbit_tree):
    p = "SAN"
    d = 0
    while 1:
        p = orbit_tree[p][0]
        if p == "COM":
            break

        orbit_tree[p][1] = d
        d += 1

    p = "YOU"
    d = 0
    while 1:
        p, _d = orbit_tree[p]
        if _d is not None:
            return d + _d - 1
        d += 1


def main():
    with open(sys.argv[1], "r") as f:
        print(transfer_distance(make_tree_from_input(f.readlines())))


main()

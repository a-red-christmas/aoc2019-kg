# The orbits form a tree and we are asked to sum up the depths to all the
# nodes.
# One way of computing this sum with O(n) complexity is to do a BF traversal of the
# tree. At each node simply mark the depth of the node and add that to a global
# sum we keep, which is the orbit check sum

# We implement the tree as a map. Key = node id, value is a list of children

import sys
from collections import deque


def make_tree_from_input(lines):
    tree = {}
    for line in lines:
        center, satellite = line.strip().split(")")
        if center not in tree:
            tree[center] = []
        tree[center] += [satellite]
    return tree


def orbit_count_checksum(orbit_tree):
    check_sum = 0
    q = deque([("COM", 0)])
    while q:
        sat = q.popleft()
        for o in orbit_tree.get(sat[0], []):
            check_sum += sat[1] + 1
            q.append((o, sat[1] + 1))
    return check_sum


def main():
    with open(sys.argv[1], "r") as f:
        print(orbit_count_checksum(make_tree_from_input(f.readlines())))


main()

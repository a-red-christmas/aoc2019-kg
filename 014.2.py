# I got lazy and reused the solution from part 1 and tacked on a search routine on top of that
# Starting from an initial guess for the fuel amount the routine hunts to find the max FUEL amount
# The only innovation here is the addition of a reset command to reset the supply network
import sys
from typing import Dict


class MaterialRequirement:
    def __init__(self, name, units):
        self.name = name
        self.units = units


class MaterialOrder(MaterialRequirement):
    pass


class SupplyNetworkNode:
    def __init__(self, line):
        self.name, self.unit_order, self.requirements = self._parse_input(line)
        self.demand: Dict[str, int] = {}

    @staticmethod
    def _parse_input(line):
        def _split_cost_item(_v: str):
            _cost, _item = _v.strip().split()
            return _item, int(_cost)

        if line == "ORE":  # Special treatment for root node
            return "ORE", 1, []

        lhs, rhs = line.strip().split("=>")
        name, unit_order = _split_cost_item(rhs)

        requirements = [
            MaterialRequirement(*_split_cost_item(requirement))
            for requirement in lhs.split(",")
        ]
        return name, unit_order, requirements

    def revise_order(self, order: MaterialOrder, supply_network: Dict[str, 'SupplyNetworkNode']):
        self.demand[order.name] = order.units

        unit_multiplier = self._get_unit_multiplier()

        for req in self.requirements:
            supply_network[req.name].revise_order(
                MaterialOrder(self.name, unit_multiplier * req.units),
                supply_network)

    def total_demand(self):
        return self._get_unit_multiplier() * self.unit_order

    def _get_unit_multiplier(self):
        raw_demand = sum(self.demand.values())
        return raw_demand // self.unit_order + (1 if raw_demand % self.unit_order > 0 else 0)

    def __str__(self):
        return f"{self.name}: {self.total_demand()}"

    def __repr__(self):
        return str(self)


def create_supply_network():
    network = {}
    with open(sys.argv[1], "r") as f:
        for line in f.readlines():
            sn = SupplyNetworkNode(line)
            network[sn.name] = sn
    return network


def reset(supply_network):
    for node in supply_network.values():
        node.demand = {}


def get_ore(supply_network, fuel):
    reset(supply_network)
    supply_network["FUEL"].revise_order(MaterialOrder("FUEL", fuel), supply_network)
    return supply_network["ORE"].total_demand()


class Guess:
    def __init__(self, fuel, ore):
        self.fuel, self.ore = fuel, ore

    def __str__(self):
        return f"ORE={self.ore} -> FUEL={self.fuel}"


def bracketing_bisection_search(supply_nw, g0: Guess, g1: Guess, max_ore=1000000000000):

    print(f"g0={g0}  g1={g1}")

    if g1.ore < max_ore:
        g0 = g1
        g1 = Guess(2 * g0.fuel, get_ore(supply_nw, 2 * g0.fuel))
        return bracketing_bisection_search(supply_nw, g0, g1, max_ore)

    if g0.fuel + 1 == g1.fuel:
        if g1.ore == max_ore:
            return g1.fuel
        else:
            return g0.fuel

    f_mid = (g0.fuel + g1.fuel)//2
    g_mid = Guess(f_mid, get_ore(supply_nw, f_mid))
    if g_mid.ore == max_ore:
        return g_mid.fuel

    if g_mid.ore < max_ore:
        g0 = g_mid
        return bracketing_bisection_search(supply_nw, g0, g1, max_ore)
    else:
        g1 = g_mid
        return bracketing_bisection_search(supply_nw, g0, g1, max_ore)


def main():
    supply_nw = create_supply_network()
    supply_nw["ORE"] = SupplyNetworkNode("ORE")

    g0 = Guess(0, 0)

    max_ore = 1000000000000
    fguess = max_ore // 114125
    g1 = Guess(fguess, get_ore(supply_nw, fguess))

    g_result = bracketing_bisection_search(supply_nw, g0, g1, max_ore)

    print("FINAL ----")
    print(g_result)


main()
# One interesting aspect of this problem is the minimum integer order aspect
# (where you have to, say order at least 10 units of something to make 10
# units of something else).
#
# My approach to this problem is to have an order based approach. I create a
# network of dependencies (it's not a tree because a node can have multiple
# ancestors) and, starting from the end FUEL node I work backwards.
#
# I make repeated "order" calls that start at a given node and propagate
# up the supply chain augmenting orders as needed. The runs stop when we
# are done processing all nodes

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

    def _get_unit_multiplier(self):
        raw_demand = sum(self.demand.values())
        return raw_demand // self.unit_order + (1 if raw_demand % self.unit_order > 0 else 0)

    def __str__(self):
        return f"{self.name}: {self._get_unit_multiplier() * self.unit_order}"

    def __repr__(self):
        return str(self)


def create_supply_network():
    network = {}
    with open(sys.argv[1], "r") as f:
        for line in f.readlines():
            sn = SupplyNetworkNode(line)
            network[sn.name] = sn
    return network


def main():
    supply_nw = create_supply_network()
    supply_nw["ORE"] = SupplyNetworkNode("ORE")
    supply_nw["FUEL"].revise_order(MaterialOrder("FUEL", 1), supply_nw)
    print(supply_nw)


main()
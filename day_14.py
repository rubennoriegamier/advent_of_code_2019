import fileinput
import re
from bisect import bisect_left
from collections import Counter
from operator import methodcaller


def main():
    reactions = parse_raw_reactions(fileinput.input())
    nanofactory = Nanofactory(reactions)
    print(nanofactory[1])
    print(bisect_left(nanofactory, 1_000_000_000_000, 1, 1_000_000_000_001) - 1)


class Nanofactory:
    __slots__ = 'reactions'

    def __init__(self, reactions):
        self.reactions = reactions

    def __getitem__(self, item):
        return ores(self.reactions, 'FUEL', item)


def parse_raw_reactions(raw_reactions):
    regex = re.compile('(\\d+) ([A-Z]+)')
    reactions = {}
    for raw_reaction in raw_reactions:
        *input_chemicals, output_chemical = regex.finditer(raw_reaction)
        output_chemical_quantity = int(output_chemical.group(1))
        output_chemical = output_chemical.group(2)
        input_chemicals = tuple((int(input_chemical_quantity), input_chemical)
                                for input_chemical_quantity, input_chemical
                                in map(methodcaller('groups'), input_chemicals))
        reactions[output_chemical] = output_chemical_quantity, input_chemicals
    return reactions


def ores(reactions, chemical, required_quantity):
    remainders = Counter()

    def ores_(chemical_, required_quantity_):
        if chemical_ == 'ORE':
            return required_quantity_
        remainder = remainders.get(chemical_, 0)
        if remainder > 0:
            remainder = min(remainder, required_quantity_)
            required_quantity_ -= remainder
            remainders[chemical_] -= remainder
        if required_quantity_ == 0:
            return 0
        output_quantity, input_chemicals = reactions[chemical_]
        multiplier = (required_quantity_ + output_quantity - 1) // output_quantity
        remainders[chemical_] += output_quantity * multiplier - required_quantity_
        return sum(ores_(input_chemical, input_quantity * multiplier)
                   for input_quantity, input_chemical in input_chemicals)

    return ores_(chemical, required_quantity)


if __name__ == '__main__':
    main()

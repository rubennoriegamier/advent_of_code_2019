import fileinput
import re
from functools import reduce
from itertools import combinations, count
from math import gcd
from operator import attrgetter, sub


class Moon:
    _PARSE_REGEX = re.compile('-?\\d+')

    @classmethod
    def parse(cls, string):
        return cls(*map(int, cls._PARSE_REGEX.findall(string)))

    __slots__ = ('initial_position_x', 'initial_position_y', 'initial_position_z',
                 'position_x', 'position_y', 'position_z',
                 'velocity_x', 'velocity_y', 'velocity_z')

    def __init__(self, position_x, position_y, position_z):
        self.initial_position_x = position_x
        self.initial_position_y = position_y
        self.initial_position_z = position_z
        self.reset()

    def __repr__(self):
        return repr(((self.position_x, self.position_y, self.position_z),
                     (self.velocity_x, self.velocity_y, self.velocity_z)))

    @property
    def potentical_energy(self):
        return abs(self.position_x) + abs(self.position_y) + abs(self.position_z)

    @property
    def kinetic_energy(self):
        return abs(self.velocity_x) + abs(self.velocity_y) + abs(self.velocity_z)

    @property
    def total_energy(self):
        return self.potentical_energy * self.kinetic_energy

    def apply_gravity(self, other):
        self.velocity_x += (self.position_x < other.position_x) - (self.position_x > other.position_x)
        self.velocity_y += (self.position_y < other.position_y) - (self.position_y > other.position_y)
        self.velocity_z += (self.position_z < other.position_z) - (self.position_z > other.position_z)

    def move(self):
        self.position_x += self.velocity_x
        self.position_y += self.velocity_y
        self.position_z += self.velocity_z

    # noinspection PyAttributeOutsideInit
    def reset(self):
        self.position_x = self.initial_position_x
        self.position_y = self.initial_position_y
        self.position_z = self.initial_position_z
        self.velocity_x = 0
        self.velocity_y = 0
        self.velocity_z = 0


def main():
    moons = list(map(Moon.parse, fileinput.input()))
    print(part_1(moons, 1_000))
    for moon in moons:
        moon.reset()
    print(part_2(moons))


def part_1(moons, steps):
    moons_combinations = list(combinations(moons, 2))
    for _ in range(steps):
        for moon_a, moon_b in moons_combinations:
            moon_a.apply_gravity(moon_b)
            moon_b.apply_gravity(moon_a)
        for moon in moons:
            moon.move()
    return sum(map(attrgetter('total_energy'), moons))


def lcm(a, b):
    return a * b // gcd(a, b)


def part_2(moons):
    moons_combinations = list(combinations(moons, 2))
    moons_reset_steps = [[] for _ in range(len(moons) * 3)]
    n = 0
    for step in count(1):
        for moon_a, moon_b in moons_combinations:
            moon_a.apply_gravity(moon_b)
            moon_b.apply_gravity(moon_a)
        index = 0
        for moon in moons:
            moon.move()
            for axis in ('x', 'y', 'z'):
                moon_reset_steps = moons_reset_steps[index]
                if isinstance(moon_reset_steps, list):
                    velocity = moon.__getattribute__(f'velocity_{axis}')
                    if velocity == 0:
                        position = moon.__getattribute__(f'position_{axis}')
                        initial_position = moon.__getattribute__(f'initial_position_{axis}')
                        if position == initial_position:
                            moon_reset_steps.append(step)
                            if len(moon_reset_steps) >= 3 and len(moon_reset_steps) & 1:
                                differences = list(map(sub, moon_reset_steps[1:], moon_reset_steps))
                                half = len(differences) // 2
                                first_half = differences[:half]
                                second_half = differences[half:]
                                if first_half == second_half:
                                    moons_reset_steps[index] = sum(first_half)
                                    n += 1
                index += 1
        if n == len(moons_reset_steps):
            break
    return reduce(lcm, moons_reset_steps)


if __name__ == '__main__':
    main()

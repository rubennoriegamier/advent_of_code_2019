import fileinput
from collections import defaultdict, deque
from itertools import combinations, groupby
from math import atan2, gcd, pi
from operator import itemgetter


class Asteroid:
    __slots__ = 'y', 'x'

    def __init__(self, y, x):
        self.y = y
        self.x = x

    def __ne__(self, other):
        return self.y != other.y or self.x != other.x

    def __repr__(self):
        return repr((self.x, self.y))

    def clockwise_angle(self, other):
        y = self.y - other.y
        x = other.x - self.x
        return (450 - atan2(y, x) * 180 / pi) % 360

    def manhattan_distance(self, other):
        return abs(self.y - other.y) + abs(self.x - other.x)

    def m(self, other):
        y = other.y - self.y
        x = other.x - self.x
        gcd_ = gcd(y, x)
        return y // gcd_, x // gcd_


def main():
    map_ = list(map(str.rstrip, fileinput.input()))
    asteroids = list(get_asteroids(map_))
    visible_asteroids, laser = part_1(asteroids)
    print(visible_asteroids)
    print(part_2(asteroids, laser, 200))


def get_asteroids(map_):
    for y, row in enumerate(map_):
        for x, point in enumerate(row):
            if point == '#':
                yield Asteroid(y, x)


def part_1(asteroids):
    m = defaultdict(set)
    for asteroid_1, asteroid_2 in combinations(asteroids, 2):
        m[asteroid_1].add(asteroid_1.m(asteroid_2))
        m[asteroid_2].add(asteroid_2.m(asteroid_1))
    return max(((len(visible_asteroids), asteroid) for asteroid, visible_asteroids in m.items()), key=itemgetter(0))


def part_2(asteroids, laser, n):
    asteroids = filter(laser.__ne__, asteroids)
    asteroids = sorted(asteroids, key=lambda asteroid: (laser.clockwise_angle(asteroid),
                                                        laser.manhattan_distance(asteroid)))
    groups = list(map(deque, map(itemgetter(1), groupby(asteroids, key=laser.m))))
    while groups:
        for group in groups:
            asteroid_ = group.popleft()
            if n == 1:
                return asteroid_.x * 100 + asteroid_.y
            n -= 1
        groups = list(filter(None, groups))


if __name__ == '__main__':
    main()

import fileinput
from functools import lru_cache
from operator import methodcaller


def main():
    local_orbits = parse_local_orbits(fileinput.input())
    print(orbits_count(local_orbits))
    print(min_transfers_to_santa(local_orbits))


def parse_local_orbits(local_orbits):
    # noinspection PyTypeChecker
    return dict(map(reversed, map(methodcaller('split', ')'), map(str.rstrip, local_orbits))))


def orbits_count(local_orbits):
    @lru_cache(maxsize=None)
    def orbits_count_(object_):
        return 0 if object_ == 'COM' else 1 + orbits_count_(local_orbits[object_])

    return sum(map(orbits_count_, local_orbits))


def path_to_com(local_orbits, object_):
    local_orbit = local_orbits.get(object_)
    while local_orbit:
        yield local_orbit
        local_orbit = local_orbits.get(local_orbit)


def min_transfers_to_santa(local_orbits):
    you_to_com = list(path_to_com(local_orbits, 'YOU'))
    san_to_com = list(path_to_com(local_orbits, 'SAN'))
    common_orbits = set(you_to_com) & set(san_to_com)
    min_transfers = None
    for common_orbit in common_orbits:
        transfers = you_to_com.index(common_orbit) + san_to_com.index(common_orbit)
        if min_transfers is None or transfers < min_transfers:
            min_transfers = transfers
    return min_transfers


if __name__ == '__main__':
    main()

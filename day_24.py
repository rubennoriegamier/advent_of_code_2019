import fileinput
from itertools import chain

import numpy as np
from scipy.signal import convolve2d

EDGES = np.array([[0, 1, 0],
                  [1, 0, 1],
                  [0, 1, 0]], np.ubyte)


def main():
    grid = parse_grid()
    print(part_1(grid))


def part_1(grid):
    biodiversity_ratings = set()
    biodiversity_rating = get_biodiversity_rating(grid)
    while biodiversity_rating not in biodiversity_ratings:
        biodiversity_ratings.add(biodiversity_rating)
        grid = get_next_grid(grid)
        biodiversity_rating = get_biodiversity_rating(grid)
    return biodiversity_rating


def parse_grid():
    return np.fromiter(map({'.': 0, '#': 1}.get,
                           chain.from_iterable(map(str.rstrip,
                                                   fileinput.input()))), np.ubyte, 25).reshape((5, 5))


def get_next_grid(grid):
    edges_count = convolve2d(grid, EDGES, 'same')
    next_grid = np.zeros_like(grid)
    next_grid[np.logical_or(edges_count == 1, np.logical_and(edges_count == 2, grid == 0))] = 1
    return next_grid


def get_biodiversity_rating(grid):
    return (2 ** np.flatnonzero(grid)).sum()


if __name__ == '__main__':
    main()

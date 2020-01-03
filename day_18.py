import fileinput
from functools import lru_cache
from itertools import chain, islice
from string import ascii_lowercase
from sys import maxsize

import networkx as nx


class Triton:
    __slots__ = '_height', '_width', '_tunnels_map', '_entrance', '_keys', '_doors', '_doors_edges'

    def __init__(self, tunnels_map):
        self._height = len(tunnels_map) - 2
        self._width = len(tunnels_map[0]) - 2
        self._tunnels_map = nx.grid_2d_graph(self._height, self._width)
        self._entrance = None
        self._keys = {}
        self._doors = {}
        self._doors_edges = {}
        for y, row in enumerate(islice(tunnels_map, 1, len(tunnels_map) - 1)):
            for x, tile in enumerate(islice(row, 1, len(row) - 1)):
                if tile != '.':
                    yx = y, x
                    if tile == '#':
                        self._tunnels_map.remove_node(yx)
                    elif tile == '@':
                        self._entrance = yx
                    elif tile in ascii_lowercase:
                        self._tunnels_map.nodes[yx]['key'] = tile
                        self._keys[tile] = yx
                    else:
                        tile = tile.lower()
                        self._tunnels_map.nodes[yx]['door'] = tile
                        self._doors[tile] = yx
        self._remove_dead_ends()
        self._remove_meaningless_keys()
        self._close_doors()

    def __str__(self):
        rows = [['#'] * (self._width + 2) for _ in range(self._height + 2)]
        for (y, x), attributes in self._tunnels_map.nodes(data=True):
            if attributes:
                rows[y + 1][x + 1] = attributes.get('key') or attributes['door'].upper()
            else:
                rows[y + 1][x + 1] = '.'
        entrance_y, entrance_x = self._entrance
        rows[entrance_y + 1][entrance_x + 1] = '@'
        return '\n'.join(map(''.join, rows))

    def _remove_dead_ends(self):
        while True:
            nodes_to_remove = set()
            for node, attributes in self._tunnels_map.nodes(data=True):
                if 'key' not in attributes and node != self._entrance:
                    neighbors = 0
                    for neighbor in self._tunnels_map.adj[node]:
                        if neighbor not in nodes_to_remove:
                            neighbors += 1
                    if neighbors < 2:
                        nodes_to_remove.add(node)
                        door = attributes.get('door')
                        if door:
                            del self._doors[door]
            if not nodes_to_remove:
                break
            self._tunnels_map.remove_nodes_from(nodes_to_remove)

    def _remove_meaningless_keys(self):
        for key, door_yx in tuple(self._doors.items()):
            key_yx = self._keys[key]
            key_edges = tuple(self._tunnels_map.edges(key_yx))
            self._tunnels_map.remove_edges_from(key_edges)
            if not nx.has_path(self._tunnels_map, self._entrance, door_yx):
                del self._tunnels_map.nodes[door_yx]['door']
                del self._tunnels_map.nodes[key_yx]['key']
                del self._keys[key]
                del self._doors[key]
            self._tunnels_map.add_edges_from(key_edges)
        keys_without_door = self._keys.keys() - self._doors.keys()
        for key_without_door in keys_without_door:
            key_without_door_yx = self._keys[key_without_door]
            key_without_door_edges = tuple(self._tunnels_map.edges(key_without_door_yx))
            self._tunnels_map.remove_edges_from(key_without_door_edges)
            for key, key_yx in tuple(self._keys.items()):
                if key != key_without_door and not nx.has_path(self._tunnels_map, self._entrance, key_yx):
                    del self._tunnels_map.nodes[key_without_door_yx]['key']
                    del self._keys[key_without_door]
                    break
            self._tunnels_map.add_edges_from(key_without_door_edges)

    def _close_doors(self):
        for door, yx in self._doors.items():
            edges = tuple(self._tunnels_map.edges(yx))
            self._tunnels_map.remove_edges_from(edges)
            self._doors_edges[door] = edges

    def shortest_path_len(self):
        @lru_cache(maxsize=None)
        def shortest_path_len(yx, remaining_keys_yx):
            shortest_path_len_ = maxsize
            for index, key_yx in enumerate(remaining_keys_yx):
                new_remaining_keys_yx = remaining_keys_yx[:index] + remaining_keys_yx[index + 1:]
                keys_edges = tuple(chain.from_iterable(map(self._tunnels_map.edges, new_remaining_keys_yx)))
                self._tunnels_map.remove_edges_from(keys_edges)
                try:
                    path_len = nx.shortest_path_length(self._tunnels_map, yx, key_yx)
                except nx.NetworkXNoPath:
                    path_len = None
                self._tunnels_map.add_edges_from(keys_edges)
                if path_len:
                    if new_remaining_keys_yx:
                        key = self._tunnels_map.nodes[key_yx]['key']
                        door_edges = self._doors_edges.get(key)
                        if door_edges:
                            self._tunnels_map.add_edges_from(door_edges)
                        shortest_path_len_ = min(shortest_path_len_,
                                                 path_len + shortest_path_len(key_yx, new_remaining_keys_yx))
                        if door_edges:
                            self._tunnels_map.remove_edges_from(door_edges)
                    else:
                        shortest_path_len_ = path_len
            return shortest_path_len_

        return shortest_path_len(self._entrance, tuple(self._keys.values()))

    def parallel_shortest_path_len(self):
        # noinspection PyShadowingNames
        @lru_cache(maxsize=None)
        def parallel_shortest_path_len(robots_yx, remaining_keys_yx):
            shortest_path_len = maxsize
            for index, key_yx in enumerate(remaining_keys_yx):
                key_y, key_x = key_yx
                # ---------
                # | 0 | 1 |
                # ---------
                # | 2 | 3 |
                # ---------
                quadrant_y = key_y > self._height / 2
                quadrant_x = key_x > self._width / 2
                quadrant_index = quadrant_y * 2 + quadrant_x
                new_remaining_keys_yx = remaining_keys_yx[:index] + remaining_keys_yx[index + 1:]
                quadrant_keys_yx = (remaining_key_yx for remaining_key_yx in new_remaining_keys_yx if
                                    (remaining_key_yx[0] > self._height / 2) == quadrant_y and
                                    (remaining_key_yx[1] > self._width / 2) == quadrant_x)
                keys_edges = tuple(chain.from_iterable(map(self._tunnels_map.edges, quadrant_keys_yx)))
                self._tunnels_map.remove_edges_from(keys_edges)
                try:
                    path_len = nx.shortest_path_length(self._tunnels_map, robots_yx[quadrant_index], key_yx)
                except nx.NetworkXNoPath:
                    path_len = None
                self._tunnels_map.add_edges_from(keys_edges)
                if path_len:
                    if new_remaining_keys_yx:
                        key = self._tunnels_map.nodes[key_yx]['key']
                        door_edges = self._doors_edges.get(key)
                        if door_edges:
                            self._tunnels_map.add_edges_from(door_edges)
                        new_robots_yxz = robots_yx[:quadrant_index] + (key_yx,) + robots_yx[quadrant_index + 1:]
                        shortest_path_len = min(shortest_path_len,
                                                path_len + parallel_shortest_path_len(new_robots_yxz,
                                                                                      new_remaining_keys_yx))
                        if door_edges:
                            self._tunnels_map.remove_edges_from(door_edges)
                    else:
                        shortest_path_len = path_len
            return shortest_path_len

        entrance_y, entrance_x = self._entrance
        robots_yx = ((entrance_y - 1, entrance_x - 1), (entrance_y - 1, entrance_x + 1),
                     (entrance_y + 1, entrance_x - 1), (entrance_y + 1, entrance_x + 1))
        quadrants_edges = tuple(chain(self._tunnels_map.edges((entrance_y - 1, entrance_x)),
                                      self._tunnels_map.edges((entrance_y + 1, entrance_x)),
                                      self._tunnels_map.edges((entrance_y, entrance_x - 1)),
                                      self._tunnels_map.edges((entrance_y, entrance_x + 1))))
        self._tunnels_map.remove_edges_from(quadrants_edges)
        shortest_path_len = parallel_shortest_path_len(robots_yx, tuple(self._keys.values()))
        self._tunnels_map.add_edges_from(quadrants_edges)
        return shortest_path_len

    @classmethod
    def parse(cls, tunnels_map):
        return cls(tuple(map(str.rstrip, tunnels_map)))


def main():
    triton = Triton.parse(fileinput.input())
    print(triton.shortest_path_len())
    print(triton.parallel_shortest_path_len())


if __name__ == '__main__':
    main()

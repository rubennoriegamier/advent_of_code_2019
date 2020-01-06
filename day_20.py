import fileinput
from collections import defaultdict
from itertools import zip_longest

import networkx as nx


def main():
    maze = Maze.parse(fileinput.input())
    print(maze.shortest_path_len())
    print(maze.recursive_shortest_path_len(), sep='\n')


class Maze:
    __slots__ = '_maze', '_entrance', '_exit', '_portal_edges', '_inner_portals', '_outer_portals'

    def __init__(self, rows):
        height = len(rows)
        width = max(map(len, rows))
        self._maze = nx.grid_2d_graph(height, width)
        self._portal_edges = []
        self._inner_portals = {}
        self._outer_portals = {}
        portals = defaultdict(list)
        for y, row in enumerate(rows):
            for x, tile in zip_longest(range(width), row, fillvalue=' '):
                node = y, x
                if tile == '.':
                    if y >= 2 and 65 <= ord(rows[y - 1][x]) <= 90:
                        label = rows[y - 2][x] + rows[y - 1][x]
                        portals[label].append(node)
                        if y == 2:
                            self._outer_portals[label] = node
                        else:
                            self._inner_portals[label] = node
                    elif y <= height - 3 and 65 <= ord(rows[y + 1][x]) <= 90:
                        label = rows[y + 1][x] + rows[y + 2][x]
                        portals[label].append(node)
                        if y == height - 3:
                            self._outer_portals[label] = node
                        else:
                            self._inner_portals[label] = node
                    elif x >= 2 and 65 <= ord(row[x - 1]) <= 90:
                        label = row[x - 2] + row[x - 1]
                        portals[label].append(node)
                        if x == 2:
                            self._outer_portals[label] = node
                        else:
                            self._inner_portals[label] = node
                    elif x <= width - 3 and 65 <= ord(row[x + 1]) <= 90:
                        label = row[x + 1] + row[x + 2]
                        portals[label].append(node)
                        if x == width - 3:
                            self._outer_portals[label] = node
                        else:
                            self._inner_portals[label] = node
                else:
                    self._maze.remove_node(node)
        if self._outer_portals.pop('AA', None) is None:
            del self._inner_portals['AA']
        if self._outer_portals.pop('ZZ', None) is None:
            del self._inner_portals['ZZ']
        portals['AA'].append(None)
        portals['ZZ'].append(None)
        for label, (portal_a, portal_b) in portals.items():
            self._maze.nodes[portal_a]['portal'] = label
            if label == 'AA':
                self._entrance = portal_a
            elif label == 'ZZ':
                self._exit = portal_a
            else:
                self._maze.nodes[portal_b]['portal'] = label
                self._portal_edges.append((portal_a, portal_b))
        self._remove_dead_ends()

    def _remove_dead_ends(self):
        while True:
            nodes_to_remove = set()
            for node, portal in self._maze.nodes(data='portal'):
                if portal is None:
                    neighbors = 0
                    for neighbor in self._maze.adj[node]:
                        if neighbor not in nodes_to_remove:
                            neighbors += 1
                    if neighbors < 2:
                        nodes_to_remove.add(node)
            if not nodes_to_remove:
                break
            self._maze.remove_nodes_from(nodes_to_remove)

    def shortest_path_len(self):
        self._maze.add_edges_from(self._portal_edges)
        shortest_path_len = nx.shortest_path_length(self._maze, self._entrance, self._exit)
        self._maze.remove_edges_from(self._portal_edges)
        return shortest_path_len

    def recursive_shortest_path_len(self):
        z = 0
        entrance_y, entrance_x = self._entrance
        exit_y, exit_x = self._exit
        floors = nx.Graph()
        floors.add_nodes_from((z, y, x) for y, x in self._maze)
        floors.add_edges_from(((z, y_1, x_1), (z, y_2, x_2)) for (y_1, x_1), (y_2, x_2) in self._maze.edges)
        path_len = None
        while path_len is None:
            z += 1
            floors.add_nodes_from((z, y, x) for y, x in self._maze)
            floors.add_edges_from(((z, y_1, x_1), (z, y_2, x_2))
                                  for (y_1, x_1), (y_2, x_2) in self._maze.edges)
            for label, (inner_y, inner_x) in self._inner_portals.items():
                outer_y, outer_x = self._outer_portals[label]
                floors.add_edge((z, outer_y, outer_x), (z - 1, inner_y, inner_x))
            try:
                path_len = nx.shortest_path_length(floors, (0, entrance_y, entrance_x), (0, exit_y, exit_x))
            except nx.NetworkXNoPath:
                pass
        return path_len

    @classmethod
    def parse(cls, string):
        return cls(tuple(map(str.rstrip, string)))


if __name__ == '__main__':
    main()

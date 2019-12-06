class Point:
    __slots__ = '_x', '_y'

    def __init__(self, x, y):
        self._x = x
        self._y = y

    def __lt__(self, other):
        return (self._x, self._y) < (other.x, other.y)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def manhattan_distance(self):
        return abs(self._x) + abs(self._y)


class Segment:
    __slots__ = '_point_a', '_point_b'

    def __init__(self, point_a, point_b):
        self._point_a = point_a
        self._point_b = point_b

    def __len__(self):
        return abs(self._point_a.x - self._point_b.x) + abs(self._point_a.y - self._point_b.y)

    @property
    def point_a(self):
        return self._point_a

    @property
    def point_b(self):
        return self._point_b

    @property
    def vertical(self):
        return self._point_a.x == self._point_b.x

    def intersection(self, other):
        self_point_a = self._point_a
        self_point_b = self._point_b
        other_point_a = other.point_a
        other_point_b = other.point_b
        if self_point_b < self_point_a:
            self_point_a, self_point_b = self_point_b, self_point_a
        if other_point_b < other_point_a:
            other_point_a, other_point_b = other_point_b, other_point_a
        if self.vertical:
            x = self_point_a.x
            if other.vertical:
                if x == other_point_a.x:
                    y_bottom = max(self_point_a.y, other_point_a.y)
                    y_top = min(self_point_b.y, other_point_b.y)
                    if y_bottom == y_top and (x or y_bottom):
                        return Point(x, y_bottom)
            else:
                y = other.point_a.y
                if other_point_a.x <= x <= other_point_b.x and self_point_a.y <= y <= self_point_b.y and (x or y):
                    return Point(x, y)
        elif other.vertical:
            y = self_point_a.y
            x = other_point_a.x
            if other_point_a.y <= y <= other_point_b.y and self_point_a.x <= x <= self_point_b.x and (x or y):
                return Point(x, y)
        else:
            y = self_point_a.y
            if y == other_point_a.y:
                x_left = max(self_point_a.x, other_point_a.x)
                x_right = min(self_point_b.x, other_point_b.x)
                if x_left == x_right and (x_left or y):
                    return Point(x_left, y)


def main():
    print(*min_manhattan_distance_and_fewest_combined_steps(input(), input()), sep='\n')


def parse_wire(wire):
    x_multiplier = {'L': -1, 'R': 1}
    y_multiplier = {'D': -1, 'U': 1}
    curr_point = Point(0, 0)
    for instruction in wire.split(','):
        direction = instruction[0]
        steps = int(instruction[1:])
        x = curr_point.x + steps * x_multiplier.get(direction, 0)
        y = curr_point.y + steps * y_multiplier.get(direction, 0)
        next_point = Point(x, y)
        yield Segment(curr_point, next_point)
        curr_point = next_point


def min_manhattan_distance_and_fewest_combined_steps(wire_a, wire_b):
    wire_a = parse_wire(wire_a)
    wire_b = list(parse_wire(wire_b))
    min_manhattan_distance = None
    fewest_combined_steps = None
    steps_a = 0
    for segment_a in wire_a:
        steps_b = 0
        for segment_b in wire_b:
            intersection = segment_a.intersection(segment_b)
            if intersection:
                manhattan_distance = intersection.manhattan_distance
                if min_manhattan_distance is None or manhattan_distance < min_manhattan_distance:
                    min_manhattan_distance = manhattan_distance
                combined_steps = (steps_a + steps_b +
                                  abs(intersection.x - segment_a.point_a.x) +
                                  abs(intersection.x - segment_b.point_a.x) +
                                  abs(intersection.y - segment_a.point_a.y) +
                                  abs(intersection.y - segment_b.point_a.y))
                if fewest_combined_steps is None or combined_steps < fewest_combined_steps:
                    fewest_combined_steps = combined_steps
            steps_b += len(segment_b)
        steps_a += len(segment_a)
    return min_manhattan_distance, fewest_combined_steps


if __name__ == '__main__':
    main()

from operator import add, mul, not_, lt, eq


def main():
    memory = list(map(int, input().split(',')))
    repair_droid = RepairDroid(memory)
    repair_droid.oxygen_shortest_path()
    print(len(repair_droid.oxygen_shortest_path()) - 1)
    print(repair_droid.oxygen_propagation_time())


class Program:
    _OPERATORS = {1: add, 2: mul, 5: bool, 6: not_, 7: lt, 8: eq}

    __slots__ = '_memory', '_pointer', '_relative_base'

    def __init__(self, memory, copy_memory=True, pointer=0, relative_base=0):
        if isinstance(memory, dict):
            self._memory = memory.copy() if copy_memory else memory
        else:
            self._memory = dict(enumerate(memory))
        self._pointer = pointer
        self._relative_base = relative_base

    def __call__(self, input_=None):
        outputs = []
        modes_and_opcode = str(self._memory.get(self._pointer, 0)).rjust(5, '0')
        opcode = int(modes_and_opcode[-2:])
        while opcode != 99:
            param_1 = self._memory.get(self._pointer + 1, 0)
            mode_3, mode_2, mode_1 = map(int, modes_and_opcode[:3])
            if opcode == 1 or opcode == 2:
                param_2 = self._memory.get(self._pointer + 2, 0)
                param_3 = self._memory.get(self._pointer + 3, 0)
                operator = self._OPERATORS[opcode]
                operand_1 = self._get_value(param_1, mode_1)
                operand_2 = self._get_value(param_2, mode_2)
                result = operator(operand_1, operand_2)
                address = self._get_address(param_3, mode_3)
                self._memory[address] = result
                self._pointer += 4
            elif opcode == 3:
                if input_ is None:
                    break
                address = self._get_address(param_1, mode_1)
                self._memory[address] = input_
                self._pointer += 2
                input_ = None
            elif opcode == 4:
                output = self._get_value(param_1, mode_1)
                outputs.append(output)
                self._pointer += 2
            elif opcode == 5 or opcode == 6:
                param_2 = self._memory.get(self._pointer + 2, 0)
                operator = self._OPERATORS[opcode]
                operand = self._get_value(param_1, mode_1)
                result = operator(operand)
                if result:
                    self._pointer = self._get_value(param_2, mode_2)
                else:
                    self._pointer += 3
            elif opcode == 7 or opcode == 8:
                param_2 = self._memory.get(self._pointer + 2, 0)
                param_3 = self._memory.get(self._pointer + 3, 0)
                operator = self._OPERATORS[opcode]
                operand_1 = self._get_value(param_1, mode_1)
                operand_2 = self._get_value(param_2, mode_2)
                result = int(operator(operand_1, operand_2))
                address = self._get_address(param_3, mode_3)
                self._memory[address] = result
                self._pointer += 4
            elif opcode == 9:
                relative_base_increment = self._get_value(param_1, mode_1)
                self._relative_base += relative_base_increment
                self._pointer += 2
            modes_and_opcode = str(self._memory.get(self._pointer, 0)).rjust(5, '0')
            opcode = int(modes_and_opcode[-2:])
        return outputs

    def _get_address(self, param, mode):
        return param if mode == 0 else self._relative_base + param

    def _get_value(self, param, mode):
        if mode == 0:
            return self._memory.get(param, 0)
        elif mode == 1:
            return param
        else:
            return self._memory.get(self._relative_base + param, 0)


class RepairDroid:
    __slots__ = '_program', '_walls', '_oxygen_shortest_path'

    def __init__(self, memory):
        self._program = Program(memory)
        self._walls = set()
        self._oxygen_shortest_path = None

    def _move_north(self, path):
        xy = path[-1][0], path[-1][1] - 1
        if xy not in self._walls and xy not in path:
            status_code = self._program(1)[0]
            if status_code == 0:
                self._walls.add(xy)
            elif status_code == 1:
                path.append(xy)
                self._move_north(path)
                self._move_west(path)
                self._move_east(path)
                path.pop()
                self._program(2)
            elif status_code == 2:
                path.append(xy)
                if self._oxygen_shortest_path is None or len(path) < len(self._oxygen_shortest_path):
                    self._oxygen_shortest_path = path.copy()
                self._move_north(path)
                self._move_west(path)
                self._move_east(path)
                path.pop()
                self._program(2)

    def _move_south(self, path):
        xy = path[-1][0], path[-1][1] + 1
        if xy not in self._walls and xy not in path:
            status_code = self._program(2)[0]
            if status_code == 0:
                self._walls.add(xy)
            elif status_code == 1:
                path.append(xy)
                self._move_south(path)
                self._move_west(path)
                self._move_east(path)
                path.pop()
                self._program(1)
            elif status_code == 2:
                path.append(xy)
                if self._oxygen_shortest_path is None or len(path) < len(self._oxygen_shortest_path):
                    self._oxygen_shortest_path = path.copy()
                self._move_south(path)
                self._move_west(path)
                self._move_east(path)
                path.pop()
                self._program(1)

    def _move_west(self, path):
        xy = path[-1][0] - 1, path[-1][1]
        if xy not in self._walls and xy not in path:
            status_code = self._program(3)[0]
            if status_code == 0:
                self._walls.add(xy)
            elif status_code == 1:
                path.append(xy)
                self._move_north(path)
                self._move_south(path)
                self._move_west(path)
                path.pop()
                self._program(4)
            elif status_code == 2:
                path.append(xy)
                if self._oxygen_shortest_path is None or len(path) < len(self._oxygen_shortest_path):
                    self._oxygen_shortest_path = path.copy()
                self._move_north(path)
                self._move_south(path)
                self._move_west(path)
                path.pop()
                self._program(4)

    def _move_east(self, path):
        xy = path[-1][0] + 1, path[-1][1]
        if xy not in self._walls and xy not in path:
            status_code = self._program(4)[0]
            if status_code == 0:
                self._walls.add(xy)
            elif status_code == 1:
                path.append(xy)
                self._move_north(path)
                self._move_south(path)
                self._move_east(path)
                path.pop()
                self._program(3)
            elif status_code == 2:
                path.append(xy)
                if self._oxygen_shortest_path is None or len(path) < len(self._oxygen_shortest_path):
                    self._oxygen_shortest_path = path.copy()
                self._move_north(path)
                self._move_south(path)
                self._move_east(path)
                path.pop()
                self._program(3)

    def oxygen_shortest_path(self):
        path = [(0, 0)]
        self._move_north(path)
        self._move_south(path)
        self._move_west(path)
        self._move_east(path)
        return self._oxygen_shortest_path

    def oxygen_propagation_time(self):
        directions = (0, -1), (0, 1), (-1, 0), (1, 0)
        oxygen = self._oxygen_shortest_path[-1]
        oxygen_tiles = {oxygen}
        adjacent_tiles = ((oxygen[0] + x_increment, oxygen[1] + y_increment) for x_increment, y_increment in directions)
        adjacent_tiles = {xy for xy in adjacent_tiles if xy not in self._walls}
        minutes = 0
        while adjacent_tiles:
            oxygen_tiles.update(adjacent_tiles)
            minutes += 1
            new_adjacent_tiles = ((oxygen_x + x_increment, oxygen_y + y_increment)
                                  for oxygen_x, oxygen_y in adjacent_tiles
                                  for x_increment, y_increment in directions)
            adjacent_tiles = {xy for xy in new_adjacent_tiles if xy not in self._walls and xy not in oxygen_tiles}
        return minutes


if __name__ == '__main__':
    main()

from operator import add, mul, not_, lt, eq, itemgetter


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

    def __call__(self, input_):
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

    @property
    def halts(self):
        return self._memory[self._pointer] == 99


class Robot:
    _ROTATIONS = {'^': ('<', '>'), '>': ('^', 'v'), 'v': ('>', '<'), '<': ('v', '^')}
    _MOVEMENTS = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}

    __slots__ = '_program', '_panels', '_position', '_direction'

    def __init__(self, memory, start_color):
        self._program = Program(memory)
        self._panels = {}
        self._position = (0, 0)
        self._direction = '^'
        self._panels[self._position] = start_color

    def __repr__(self):
        white_panels = {(y, x) for (y, x), color in self._panels.items() if color == 1}
        min_y = min(map(itemgetter(0), white_panels))
        max_y = max(map(itemgetter(0), white_panels))
        min_x = min(map(itemgetter(1), white_panels))
        max_x = max(map(itemgetter(1), white_panels))
        canvas = [[' ' for _ in range(max_x - min_x + 1)] for _ in range(max_y - min_y + 1)]
        for y, x in white_panels:
            canvas[y - min_y][x - min_x] = '#'
        return '\n'.join(map(''.join, canvas))

    def _rotate(self, turn):
        self._direction = self._ROTATIONS[self._direction][turn]

    def _move(self):
        self._position = tuple(map(sum, zip(self._position, self._MOVEMENTS[self._direction])))

    @property
    def painted_panels(self):
        return len(self._panels)

    def paint(self):
        while not self._program.halts:
            curr_color = self._panels.get(self._position, 0)
            new_color, turn = self._program(curr_color)
            self._panels[self._position] = new_color
            self._rotate(turn)
            self._move()


def main():
    memory = list(map(int, input().split(',')))
    robot = Robot(memory, 0)
    robot.paint()
    print(robot.painted_panels)
    robot = Robot(memory, 1)
    robot.paint()
    print(robot)


if __name__ == '__main__':
    main()

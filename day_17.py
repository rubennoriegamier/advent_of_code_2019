from itertools import chain, islice
from operator import add, mul, not_, lt, eq


def main():
    memory = list(map(int, input().split(',')))
    calibration, rows = calibrate(memory)
    print(calibration)
    dust = collect_dust(memory, rows)
    print(dust)


def calibrate(memory):
    calibration = 0
    program = Program(memory)
    rows = ''.join(map(chr, program())).rstrip().split('\n')
    for curr_row_number, curr_row in enumerate(islice(rows, 1, len(rows) - 1), 1):
        prev_row = rows[curr_row_number - 1]
        next_row = rows[curr_row_number + 1]
        for curr_col_number, curr_tile in enumerate(islice(curr_row, 1, len(curr_row) - 1), 1):
            if (curr_tile != '.' and
                    prev_row[curr_col_number] != '.' and
                    next_row[curr_col_number] != '.' and
                    curr_row[curr_col_number - 1] != '.' and
                    curr_row[curr_col_number + 1] != '.'):
                calibration += curr_row_number * curr_col_number
    return calibration, rows


def collect_dust(memory, rows):
    memory[0] = 2
    instructions = get_instructions(rows)
    main_routine_and_functions = get_main_routine_and_functions(instructions)
    program = Program(memory)
    program()
    for input_ in chain.from_iterable(main_routine_and_functions):
        program(input_)
    program(ord('n'))
    return program(ord('\n'))[-1]


def get_instructions(rows):
    scaffolds = set()
    robot_x = None
    robot_y = None
    direction = None
    for row_number, row in enumerate(rows):
        for col_number, tile in enumerate(row):
            if tile != '.':
                scaffolds.add((col_number, row_number))
                if tile != '#':
                    robot_x = col_number
                    robot_y = row_number
                    direction = tile
    instructions = []
    while direction:
        if direction == '^':
            if (robot_x - 1, robot_y) in scaffolds:
                direction = '<'
                instructions.append('L')
                instructions.append(1)
                robot_x -= 1
                while (robot_x - 1, robot_y) in scaffolds:
                    instructions[-1] += 1
                    robot_x -= 1
            elif (robot_x + 1, robot_y) in scaffolds:
                direction = '>'
                instructions.append('R')
                instructions.append(1)
                robot_x += 1
                while (robot_x + 1, robot_y) in scaffolds:
                    instructions[-1] += 1
                    robot_x += 1
            else:
                direction = None
        elif direction == 'v':
            if (robot_x - 1, robot_y) in scaffolds:
                direction = '<'
                instructions.append('R')
                instructions.append(1)
                robot_x -= 1
                while (robot_x - 1, robot_y) in scaffolds:
                    instructions[-1] += 1
                    robot_x -= 1
            elif (robot_x + 1, robot_y) in scaffolds:
                direction = '>'
                instructions.append('L')
                instructions.append(1)
                robot_x += 1
                while (robot_x + 1, robot_y) in scaffolds:
                    instructions[-1] += 1
                    robot_x += 1
            else:
                direction = None
        elif direction == '<':
            if (robot_x, robot_y - 1) in scaffolds:
                direction = '^'
                instructions.append('R')
                instructions.append(1)
                robot_y -= 1
                while (robot_x, robot_y - 1) in scaffolds:
                    instructions[-1] += 1
                    robot_y -= 1
            elif (robot_x, robot_y + 1) in scaffolds:
                direction = 'v'
                instructions.append('L')
                instructions.append(1)
                robot_y += 1
                while (robot_x, robot_y + 1) in scaffolds:
                    instructions[-1] += 1
                    robot_y += 1
            else:
                direction = None
        elif direction == '>':
            if (robot_x, robot_y - 1) in scaffolds:
                direction = '^'
                instructions.append('L')
                instructions.append(1)
                robot_y -= 1
                while (robot_x, robot_y - 1) in scaffolds:
                    instructions[-1] += 1
                    robot_y -= 1
            elif (robot_x, robot_y + 1) in scaffolds:
                direction = 'v'
                instructions.append('R')
                instructions.append(1)
                robot_y += 1
                while (robot_x, robot_y + 1) in scaffolds:
                    instructions[-1] += 1
                    robot_y += 1
            else:
                direction = None
    return tuple(zip(instructions[::2], map(str, instructions[1::2])))


def get_main_routine_and_functions(instructions):
    function_bodies = []

    def refactor_instructions():
        if len(function_bodies) <= 10:
            function_bodies_uniq = set(function_bodies)
            index_start = sum(map(len, function_bodies))
            for index_stop in range(index_start + 1, len(instructions) + 1):
                function_body = instructions[index_start:index_stop]
                function_len = sum(map(len, chain.from_iterable(function_body))) + len(function_body) * 2 - 1
                if function_len > 20:
                    break
                if function_body in function_bodies_uniq or len(function_bodies_uniq) < 3:
                    function_bodies.append(function_body)
                    if sum(map(len, function_bodies)) == len(instructions) or refactor_instructions():
                        return True
                    function_bodies.pop()

    refactor_instructions()
    functions = {function_body: function_name
                 for function_name, function_body in zip(('A', 'B', 'C'), set(function_bodies))}
    main_routine = list(map(functions.get, function_bodies))
    functions = [(function_name, function_body) for function_body, function_name in functions.items()]
    functions.sort()
    inputs = [main_routine]
    for (_, function_body) in functions:
        inputs.append(chain.from_iterable(function_body))
    return [list(map(ord, ','.join(input_) + '\n')) for input_ in inputs]


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


if __name__ == '__main__':
    main()

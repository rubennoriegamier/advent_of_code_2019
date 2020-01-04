from itertools import count, islice, tee
from operator import add, mul, not_, lt, eq


def main():
    # noinspection PyTypeChecker
    memory = dict(enumerate(map(int, input().split(','))))
    tractor_beam = TractorBeam(memory)
    print(part_1(tractor_beam))
    print(part_2(tractor_beam))


def part_1(tractor_beam):
    return sum(min(x_stop, 50) - x_start for x_start, x_stop in islice(tractor_beam, 50))


def part_2(tractor_beam):
    x_start_stop_1, x_start_stop_2 = tee(tractor_beam)
    x_start_stop_2 = islice(x_start_stop_2, 99, None)
    for (y, (x_start_1, x_stop_1)), (x_start_2, x_stop_2) in zip(enumerate(x_start_stop_1), x_start_stop_2):
        if x_stop_1 - x_start_2 >= 100 and x_start_1 <= x_start_2 < x_stop_1 and x_start_2 <= x_stop_1 < x_stop_2:
            return x_start_2 * 10_000 + y


class TractorBeam:
    __slots__ = '_memory'

    def __init__(self, memory):
        self._memory = memory

    def __getitem__(self, xy):
        x, y = xy
        memory = self._memory.copy()
        program = Program(memory)
        program(x)
        return program(y)[0]

    def __iter__(self):
        x_start = 0
        x_stop = 1
        for y in count():
            if not self[x_start, y]:
                x_start += 1
                x_stop += 1
            if self[x_stop, y]:
                x_stop += 1
            elif x_start < x_stop and not self[x_stop - 1, y]:
                x_stop -= 1
            yield x_start, x_stop


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

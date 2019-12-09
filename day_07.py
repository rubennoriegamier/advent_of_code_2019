from copy import copy
from itertools import permutations
from operator import add, mul, not_, lt, eq


class Program:
    _OPERATORS = {1: add, 2: mul, 5: bool, 6: not_, 7: lt, 8: eq}

    __slots__ = '_memory', '_pointer'

    def __init__(self, memory, copy_memory=True, pointer=0):
        self._memory = memory.copy() if copy_memory else memory
        self._pointer = pointer

    def __call__(self, input_):
        outputs = []
        modes_and_opcode = str(self._memory[self._pointer]).rjust(4, '0')
        opcode = int(modes_and_opcode[-2:])
        mode_2, mode_1 = map(int, modes_and_opcode[:2])
        while opcode != 99:
            param_1 = self._memory[self._pointer + 1]
            if opcode == 1 or opcode == 2:
                param_2 = self._memory[self._pointer + 2]
                param_3 = self._memory[self._pointer + 3]
                operator = self._OPERATORS[opcode]
                operand_1 = self._memory[param_1] if mode_1 == 0 else param_1
                operand_2 = self._memory[param_2] if mode_2 == 0 else param_2
                self._memory[param_3] = operator(operand_1, operand_2)
                self._pointer += 4
            elif opcode == 3:
                if input_ is None:
                    break
                self._memory[param_1] = input_
                self._pointer += 2
                input_ = None
            elif opcode == 4:
                output = self._memory[param_1] if mode_1 == 0 else param_1
                outputs.append(output)
                self._pointer += 2
            elif opcode == 5 or opcode == 6:
                operator = self._OPERATORS[opcode]
                if operator(self._memory[param_1] if mode_1 == 0 else param_1):
                    param_2 = self._memory[self._pointer + 2]
                    self._pointer = self._memory[param_2] if mode_2 == 0 else param_2
                else:
                    self._pointer += 3
            elif opcode == 7 or opcode == 8:
                operator = self._OPERATORS[opcode]
                param_2 = self._memory[self._pointer + 2]
                param_3 = self._memory[self._pointer + 3]
                self._memory[param_3] = int(operator(self._memory[param_1] if mode_1 == 0 else param_1,
                                                     self._memory[param_2] if mode_2 == 0 else param_2))
                self._pointer += 4
            modes_and_opcode = str(self._memory[self._pointer]).rjust(4, '0')
            opcode = int(modes_and_opcode[-2:])
            mode_2, mode_1 = map(int, modes_and_opcode[:2])
        return outputs

    def __copy__(self):
        return type(self)(self._memory, pointer=self._pointer)

    @property
    def halts(self):
        return self._memory[self._pointer] == 99


def main():
    memory = list(map(int, input().split(',')))
    print(part_1(memory))
    print(part_2(memory))


def part_1(memory):
    programs = [Program(memory) for _ in range(5)]
    for phase, program in enumerate(programs):
        program(phase)
    highest_signal = 0
    cached_signals = [{} for _ in range(5)]
    for phases in permutations(range(5)):
        curr_signal = 0
        for phase in phases:
            next_signal = cached_signals[phase].get(curr_signal)
            if next_signal is None:
                program = copy(programs[phase])
                next_signal = program(curr_signal)[0]
                cached_signals[phase][curr_signal] = next_signal
            curr_signal = next_signal
        highest_signal = max(curr_signal, highest_signal)
    return highest_signal


def part_2(memory):
    programs = [Program(memory) for _ in range(5, 10)]
    for phase, program in enumerate(programs, 5):
        program(phase)
    highest_signal = 0
    for phases in permutations(range(5, 10)):
        curr_signal = 0
        programs_ = list(map(copy, programs))
        while not programs_[-1].halts:
            for phase in phases:
                program = programs_[phase - 5]
                curr_signal = program(curr_signal)[0]
        highest_signal = max(curr_signal, highest_signal)
    return highest_signal


if __name__ == '__main__':
    main()

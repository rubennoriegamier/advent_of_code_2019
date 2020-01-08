from operator import add, mul, not_, lt, eq, itemgetter

WALK_SCRIPTS = [('NOT A J', 'WALK'),
                ('NOT B T', 'NOT C J', 'AND T J', 'NOT A T', 'OR T J', 'AND D J', 'WALK'),
                ('NOT B J', 'NOT A T', 'OR T J', 'AND D J', 'WALK'),
                ('NOT C J', 'NOT A T', 'OR T J', 'AND D J', 'WALK')]
RUN_SCRIPTS = [('OR D T', 'AND H T', 'OR D J', 'AND E J', 'AND I J', 'OR T J', 'AND A T', 'AND B T', 'AND C T',
                'NOT T T', 'AND T J', 'NOT A T', 'OR T J', 'RUN')]


def main():
    memory = list(map(int, input().split(',')))
    print(get_damage(memory, WALK_SCRIPTS))
    print(get_damage(memory, RUN_SCRIPTS))


def get_damage(memory, scripts, debug=False):
    damage = 0
    for script in scripts:
        script = list(map(ord, '\n'.join(script) + '\n'))
        program = Program(memory)
        outputs = []
        for input_ in script:
            outputs.extend(program(input_))
        damage = max(damage, outputs[-1])
        if debug:
            print(*map(chr, outputs[:-1]), sep='', end='\n\n----------\n\n')
    return damage


def get_run_scripts():
    labels = 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'
    yield 'NOT A J', 'RUN'
    # for n in range(511):
    #     continue
    #     sensors = list(map(int, bin(n)[2:].rjust(9, '0')))
    #     ground = list(map(itemgetter(1), filterfalse(itemgetter(0), zip(sensors, labels))))
    #     instructions = [f'NOT {ground[0]} J']
    #     for i in range(1, len(ground)):
    #         instructions.append(f'NOT {ground[i]} T')
    #         instructions.append('AND T J')
    #     instructions.extend(('NOT A T', 'OR T J', 'AND D J', 'RUN'))
    #     yield instructions
    for n in range(1, 512):
        sensors = list(map(int, bin(n)[2:].rjust(9, '0')))
        ground = list(map(itemgetter(1), filter(itemgetter(0), zip(sensors, labels))))
        instructions = [f'OR {ground[0]} J']
        for i in range(1, len(ground)):
            instructions.append(f'AND {ground[i]} J')
        instructions.extend(('NOT A T', 'OR T J', 'AND D J', 'RUN'))
        yield instructions


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

from operator import add, mul


def main():
    memory = list(map(int, input().split(',')))
    print(part_1(memory))
    print(part_2(memory, 19_690_720))


def part_1(memory, noun=12, verb=2):
    operators = {1: add, 2: mul}
    memory = memory.copy()
    memory[1] = noun
    memory[2] = verb
    pointer = 0
    opcode = memory[pointer]
    while opcode != 99:
        param_1 = memory[pointer + 1]
        param_2 = memory[pointer + 2]
        param_3 = memory[pointer + 3]
        operator = operators[opcode]
        operand_1 = memory[param_1]
        operand_2 = memory[param_2]
        result = operator(operand_1, operand_2)
        memory[param_3] = result
        pointer += 4
        opcode = memory[pointer]
    return memory[0]


def part_2(integers, output):
    noun_0 = part_1(integers, 0, 0)
    noun_1 = part_1(integers, 1, 0)
    noun_increment = noun_1 - noun_0
    noun, verb = divmod(output - noun_0, noun_increment)
    return 100 * noun + verb


if __name__ == '__main__':
    main()

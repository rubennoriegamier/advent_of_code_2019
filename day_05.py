from operator import add, mul, truth, not_, lt, eq


def main():
    memory = list(map(int, input().split(',')))
    print(diagnostic_code(memory, 1))
    print(diagnostic_code(memory, 5))


def diagnostic_code(memory, input_id):
    operators = {1: add, 2: mul, 5: truth, 6: not_, 7: lt, 8: eq}
    memory = memory.copy()
    output = None
    pointer = 0
    modes_and_opcode = str(memory[pointer]).rjust(4, '0')
    opcode = int(modes_and_opcode[-2:])
    while opcode != 99:
        mode_1 = int(modes_and_opcode[-3])
        param_1 = memory[pointer + 1]
        if opcode == 1 or opcode == 2:
            mode_2 = int(modes_and_opcode[-4])
            param_2 = memory[pointer + 2]
            param_3 = memory[pointer + 3]
            operator = operators[opcode]
            operand_1 = memory[param_1] if mode_1 == 0 else param_1
            operand_2 = memory[param_2] if mode_2 == 0 else param_2
            result = operator(operand_1, operand_2)
            memory[param_3] = result
            pointer += 4
        elif opcode == 3:
            memory[param_1] = input_id
            pointer += 2
        elif opcode == 4:
            output = memory[param_1] if mode_1 == 0 else param_1
            pointer += 2
        elif opcode == 5 or opcode == 6:
            operator = operators[opcode]
            if operator(memory[param_1] if mode_1 == 0 else param_1):
                mode_2 = int(modes_and_opcode[-4])
                param_2 = memory[pointer + 2]
                pointer = memory[param_2] if mode_2 == 0 else param_2
            else:
                pointer += 3
        elif opcode == 7 or opcode == 8:
            operator = operators[opcode]
            mode_2 = int(modes_and_opcode[-4])
            param_2 = memory[pointer + 2]
            param_3 = memory[pointer + 3]
            memory[param_3] = int(operator(memory[param_1] if mode_1 == 0 else param_1,
                                           memory[param_2] if mode_2 == 0 else param_2))
            pointer += 4
        modes_and_opcode = str(memory[pointer]).rjust(5, '0')
        opcode = int(modes_and_opcode[-2:])
    return output


if __name__ == '__main__':
    main()

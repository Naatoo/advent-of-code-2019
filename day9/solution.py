from typing import List, Generator, Optional


def get_program() -> dict:
    with open("input.txt") as file:
        program: dict = {index: int(num) for index, num in enumerate(file.read().split(","))}
        return program


def get_score(opcode: int, input_1: int, input_2: int) -> int:
    score: int
    if opcode == 1:
        score = input_1 + input_2
    elif opcode == 2:
        score = input_1 * input_2
    return score


def intcode_computer(program: dict, input_value: int) -> List[int]:
    mapping_rel: dict = {
        1: 3,
        2: 3,
        3: 1,
        4: 1,
        7: 3,
        8: 3,
        9: 1
    }
    index: int = 0
    relative_base: int = 0
    opcode = None
    while opcode != 99:
        instruction_value: str = str(program[index])
        opcode: int = int(instruction_value[-2:])
        param_read_write_index: Optional[int] = mapping_rel.get(opcode)
        parameters: dict = {}
        for instruction_index, digit_index in enumerate(range(-3, -6, -1)):
            mode_par: int = int(instruction_value[digit_index]) if len(instruction_value) >= abs(digit_index) else 0
            rel_index: int = instruction_index + 1
            if mode_par == 0:
                parameters[rel_index] = program.get(program.get(index + rel_index, 0), 0)
                if rel_index == param_read_write_index:
                    write_read_index = lambda x: program.get(index + x, 0)
            elif mode_par == 1:
                parameters[rel_index] = program.get(index + rel_index, 0)
                if rel_index == param_read_write_index:
                    write_read_index = lambda x: index + x
            elif mode_par == 2:
                parameters[rel_index] = program.get(program.get(index + rel_index, 0) + relative_base, 0)
                if rel_index == param_read_write_index:
                    write_read_index = lambda x: program.get(index + x, 0) + relative_base
        if opcode in [1, 2]:
            write_value: int = get_score(opcode, parameters[1], parameters[2])
            write_address: int = write_read_index(3)
            program[write_address] = write_value
            index += 4
        elif opcode == 3:
            write_value: int = input_value
            write_address: int = write_read_index(1)
            index += 2
            program[write_address] = write_value
        elif opcode == 4:
            output_value: int = program.get(write_read_index(1), 0)
            index += 2
            yield output_value
        elif opcode == 5:
            index = parameters[2] if parameters[1] != 0 else index + 3
        elif opcode == 6:
            index = parameters[2] if parameters[1] == 0 else index + 3
        elif opcode == 7:
            val: int = 1 if parameters[1] < parameters[2] else 0
            program[write_read_index(3)] = val
            index += 4
        elif opcode == 8:
            val: int = 1 if parameters[1] == parameters[2] else 0
            program[write_read_index(3)] = val
            index += 4
        elif opcode == 9:
            relative_base += program.get(write_read_index(1), 0)
            index += 2
    return


def get_diagnostic_code(program: dict, input_value: int) -> List[int]:
    generated_codes_gen: Generator = intcode_computer(program, input_value)
    output_codes: List[int] = []
    for code in generated_codes_gen:
        try:
            output_codes.append(code)
        except StopIteration:
            break
    return output_codes


if __name__ == "__main__":
    part_1: List[int] = get_diagnostic_code(get_program(), input_value=1)
    print("PART1:", part_1)

    part_2: List[int] = get_diagnostic_code(get_program(), input_value=2)
    print("PART2:", part_2)

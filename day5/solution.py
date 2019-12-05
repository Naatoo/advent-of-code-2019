from typing import List, Generator


def get_program() -> List[int]:
    with open("input.txt") as file:
        program: List[int] = [int(num) for num in file.read().split(",")]
        return program


def process_program_part_1(program: List[int], input_value: int) -> List[int]:
    index: int = 0
    while True:
        instruction_value: str = str(program[index])
        opcode: int = int(instruction_value[-2:])
        if opcode == 99:
            yield 'opcode_99'
        mode_par_1, mode_par_2, mode_par_3 = (int(instruction_value[digit_index])
                                              if len(instruction_value) >= abs(digit_index) else 0
                                              for digit_index in range(-3, -6, -1))
        assert all(par in (0, 1) for par in (mode_par_1, mode_par_2, mode_par_3)), \
            f"{mode_par_1}, {mode_par_2}, {mode_par_3}"
        if opcode in [1, 2, 3]:
            if opcode in [1, 2]:
                input_1, input_2 = (program[index + instruction_index + 1] if par == 1
                                    else program[program[index + instruction_index + 1]]
                                    for instruction_index, par in enumerate((mode_par_1, mode_par_2)))
                write_value: int = get_score(opcode, input_1, input_2)
                write_address: int = program[index + 3]
                index += 4
            else:
                write_value: int = input_value
                write_address: int = program[index + 1]
                index += 2
            program[write_address] = write_value
        elif opcode == 4:
            yield_value: int = program[index + 1] if mode_par_1 == 1 else program[program[index + 1]]
            yield yield_value
            index += 2
        else:
            raise ValueError(f"Opcode={opcode} is not in (1, 2, 3, 4, 99)")


def get_score(opcode: int, input_1: int, input_2: int) -> int:
    score: int
    if opcode == 1:
        score = input_1 + input_2
    elif opcode == 2:
        score = input_1 * input_2
    return score


def get_diagnostic_code(program: List[int], input_value: int, part: int) -> int:
    func = process_program_part_1 if part == 1 else process_program_part_2
    generated_codes: Generator = func(program, input_value)
    for code in generated_codes:
        try:
            assert code == 0
        except AssertionError:
            diagnostic_code: int = code
            break
    next_code = next(generated_codes)
    if next_code == 'opcode_99':
        return diagnostic_code
    else:
        raise ValueError(f"Diagnostic_code={diagnostic_code}, next_code={next_code}")


def process_program_part_2(program: List[int], input_value: int) -> List[int]:
    index: int = 0
    while True:
        instruction_value: str = str(program[index])
        opcode: int = int(instruction_value[-2:])
        if opcode == 99:
            yield 'opcode_99'
        mode_par_1, mode_par_2, mode_par_3 = (int(instruction_value[digit_index])
                                              if len(instruction_value) >= abs(digit_index) else 0
                                              for digit_index in range(-3, -6, -1))
        assert all(par in (0, 1) for par in (mode_par_1, mode_par_2, mode_par_3)), \
            f"{mode_par_1}, {mode_par_2}, {mode_par_3}"
        input_1, input_2 = (program[index + instruction_index + 1] if par == 1
                            else program[program[index + instruction_index + 1]]
                            for instruction_index, par in enumerate((mode_par_1, mode_par_2)))
        if opcode in [1, 2, 3]:
            if opcode in [1, 2]:
                write_value: int = get_score(opcode, input_1, input_2)
                write_address: int = program[index + 3]
                index += 4
            else:
                write_value: int = input_value
                write_address: int = program[index + 1]
                index += 2
            program[write_address] = write_value
        elif opcode == 4:
            yield_value: int = program[index + 1] if mode_par_1 == 1 else program[program[index + 1]]
            yield yield_value
            index += 2
        elif opcode == 5:
            if input_1 != 0:
                index = input_2
            else:
                index += 3
        elif opcode == 6:
            if input_1 == 0:
                index = input_2
            else:
                index += 3
        elif opcode in (7, 8):
            third_param = program[index + 3]
            if opcode == 7 and input_1 < input_2:
                val: int = 1
            elif opcode == 8 and input_1 == input_2:
                val: int = 1
            else:
                val: int = 0
            program[third_param] = val
            index += 4
        else:
            raise ValueError(f"Opcode={opcode} is not in (1, 2, 3, 4, 5, 6, 7, 8 99)")


if __name__ == "__main__":
    part_1_result: int = get_diagnostic_code(get_program(), input_value=1, part=1)
    print("PART1:", part_1_result)

    part_2_result: int = get_diagnostic_code(get_program(), input_value=5, part=2)
    print("PART2:", part_2_result)

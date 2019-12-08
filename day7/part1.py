import itertools
from typing import List, Generator


def get_program() -> List[int]:
    with open("input.txt") as file:
        program: List[int] = [int(num) for num in file.read().split(",")]
        return program


def get_score(opcode: int, input_1: int, input_2: int) -> int:
    score: int
    if opcode == 1:
        score = input_1 + input_2
    elif opcode == 2:
        score = input_1 * input_2
    return score


def get_diagnostic_code_part_1(program: List[int], phase_combination, initial_input) -> int:
    func = process_program_part_1
    input_value: int = initial_input
    for phase in phase_combination:
        generated_codes: Generator = func(program, input_value, phase)
        for code in generated_codes:
            try:
                assert code == 0
            except AssertionError:
                diagnostic_code: int = code
                break
        next_code = next(generated_codes)
        if next_code == 'opcode_99':
            input_value = diagnostic_code
        else:
            raise ValueError(f"Diagnostic_code={diagnostic_code}, next_code={next_code}")
    return diagnostic_code


def get_max_signal(initial_input: int):
    signals: list = []
    for comb in itertools.permutations('01234'):
        phase_combination: list = list(map(int, list(comb)))
        signals.append(get_diagnostic_code_part_1(get_program(), phase_combination, initial_input))
    max_signal: int = max(signals)
    return max_signal


def process_program_part_1(program: List[int], input_value: int, phase: int) -> List[int]:
    index: int = 0
    input_intruction_index = 0
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
        if opcode not in [3, 4]:
            input_1, input_2 = (program[index + instruction_index + 1] if par == 1
                                else program[program[index + instruction_index + 1]]
                                for instruction_index, par in enumerate((mode_par_1, mode_par_2)))
        if opcode in [1, 2, 3]:
            if opcode in [1, 2]:
                write_value: int = get_score(opcode, input_1, input_2)
                write_address: int = program[index + 3]
                index += 4
            else:
                input_intruction_index += 1
                if input_intruction_index == 1:
                    write_value: int = phase
                elif input_intruction_index == 2:
                    write_value: int = input_value
                else:
                    raise ValueError("Opcode 3 possible only in two instructions")
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
    samples_1 = (
        ([3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0], [4, 3, 2, 1, 0]),
        ([3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23, 101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0],
         [0, 1, 2, 3, 4]),
        ([3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33, 1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31,
          31, 4, 31, 99, 0, 0, 0], [1, 0, 4, 3, 2])
    )

    for index, (sample_program, phase_comp) in enumerate(samples_1):
        sample_result: int = get_diagnostic_code_part_1(sample_program, phase_comp, initial_input=0)
        print(f"PART 1 SAMPLE {index + 1}:", sample_result)

    part_1_result: int = get_max_signal(initial_input=0)
    print("PART1:", part_1_result)

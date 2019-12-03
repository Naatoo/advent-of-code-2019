import itertools
from typing import List


def get_programs() -> List[int]:
    with open("input.txt") as file:
        program: List[int] = [int(num) for num in file.read().split(",")]
        return program


def process_program(program: List[int]) -> List[int]:
    index: int = 0
    for index in range(0, len(program), 4):
        opcode = program[index]
        if opcode == 99:
            break
        input_1_index, input_2_index, output_index = program[index + 1: index + 4]
        input_1, input_2 = program[input_1_index], program[input_2_index]
        score: int = get_score(opcode, input_1, input_2)
        program[output_index] = score
    return program


def get_score(opcode: int, input_1: int, input_2: int) -> int:
    score: int
    if opcode == 1:
        score = input_1 + input_2
    elif opcode == 2:
        score = input_1 * input_2
    else:
        raise ValueError(f"Opcode={opcode} is not in (1, 2, 99)")
    return score


def get_program_first_value(program: List[int]) -> int:
    first_value: int = program[0]
    return first_value


def get_result_first_value_19690720() -> int:
    final_noun: int
    final_verb: int
    for noun, verb in itertools.product(range(100), range(100)):
        program = get_programs()
        program[1], program[2] = noun, verb
        first_value: int = get_program_first_value(process_program(program))
        if first_value == 19690720:
            final_noun, final_verb = noun, verb
            break
    result: int = 100 * final_noun + final_verb
    return result


if __name__ == "__main__":
    sample_programs: List[List[int]] = [
        [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50],
        [1, 0, 0, 0, 99],
        [2, 3, 0, 3, 99],
        [2, 4, 4, 5, 99, 0],
        [1, 1, 1, 4, 99, 5, 6, 0, 99]
    ]
    sample_results: tuple = tuple(get_program_first_value(process_program(sample)) for sample in sample_programs)
    print("SAMPLE RESULTS:", sample_results)

    part_1_result: int = get_program_first_value(process_program(get_programs()))
    print("PART1:", part_1_result)

    part_2_result: int = get_result_first_value_4090689()
    print("PART2:", part_2_result)

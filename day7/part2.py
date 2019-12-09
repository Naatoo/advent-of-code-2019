import itertools
from typing import List, Coroutine, Union


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


def process_amplifier(program: List[int], phase: int, initial_input_value: int) -> List[int]:
    index: int = 0
    diagnostic_code: None = None
    while diagnostic_code is None:
        instruction_value: str = str(program[index])
        opcode: int = int(instruction_value[-2:])
        mode_par_1, mode_par_2, mode_par_3 = (int(instruction_value[digit_index])
                                              if len(instruction_value) >= abs(digit_index) else 0
                                              for digit_index in range(-3, -6, -1))
        if opcode not in [3, 4, 99]:
            par_1, par_2 = (program[index + instruction_index + 1] if par == 1
                                else program[program[index + instruction_index + 1]]
                                for instruction_index, par in enumerate((mode_par_1, mode_par_2)))
        if opcode in [1, 2]:
            program[program[index + 3]] = get_score(opcode, par_1, par_2)
            index += 4
        elif opcode == 3:
            if phase is not None:
                input_signal: int = phase
                phase = None
            elif initial_input_value is not None:
                input_signal: int = initial_input_value
                initial_input_value = None
            else:
                input_signal: int = yield output_signal
            program[program[index + 1]] = input_signal
            index += 2
        elif opcode == 4:
            output_signal: int = program[index + 1] if mode_par_1 == 1 else program[program[index + 1]]
            index += 2
        elif opcode == 5:
            index = par_2 if par_1 != 0 else index + 3
        elif opcode == 6:
            index = par_2 if par_1 == 0 else index + 3
        elif opcode == 7:
            program[program[index + 3]] = 1 if par_1 < par_2 else 0
            index += 4
        elif opcode == 8:
            program[program[index + 3]] = 1 if par_1 == par_2 else 0
            index += 4
        elif opcode == 99:
            diagnostic_code: int = output_signal
        else:
            raise ValueError(f"Opcode={opcode} is not in {(*range(1, 9), 99)})")
    return diagnostic_code


def get_diagnostic_code_part_2(program: List[int], phase_combination, initial_input) -> int:
    # INITIALIZE AMPLIFIERS
    amplifiers: list = []
    for amp_index in range(5):
        amp: Coroutine = process_amplifier(program, phase_combination[amp_index], initial_input)
        amplifiers.append(amp)
        initial_input: int = next(amp)

    # PROCESS PROGRAMS
    code: int = initial_input
    diagnostic_code: Union[None, int] = None
    for amp in itertools.cycle(amplifiers):
        try:
            code = amp.send(code)
        except StopIteration as e:
            if amplifiers.index(amp) == 4:
                diagnostic_code = e.value
                break
            else:
                code = e.value
    return diagnostic_code


def get_max_signal(program: list, initial_input: int):
    max_signal: int = max((get_diagnostic_code_part_2(program, tuple(map(int, list(comb))), initial_input))
                          for comb in itertools.permutations('56789'))
    return max_signal


if __name__ == "__main__":
    part_2: int = get_max_signal(program=get_program(), initial_input=0)
    print("PART2:", part_2)

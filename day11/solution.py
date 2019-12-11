import collections
import itertools
from typing import List, Optional, Coroutine


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


def intcode_computer(program: dict, initial_input_value: int) -> List[int]:
    mapping_rel: dict = {
        1: 3,
        2: 3,
        3: 1,
        4: 1,
        7: 3,
        8: 3,
        9: 1
    }
    index, relative_base = 0, 0
    opcode, color_num, dir_num = None, None, None
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
            if initial_input_value is not None:
                write_value: int = initial_input_value
                initial_input_value = None
            else:
                write_value: int = yield color_num, dir_num
                color_num = None
                dir_num = None
            write_address: int = write_read_index(1)
            index += 2
            program[write_address] = write_value
        elif opcode == 4:
            output_value: int = program.get(write_read_index(1), 0)
            index += 2
            if color_num is None:
                color_num = output_value
            elif dir_num is None:
                dir_num = output_value
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


def get_painted_fields(program: dict, initial_input_value: int) -> dict:
    painted_fields: dict = {}
    intcode_coro: Coroutine = intcode_computer(program, initial_input_value)
    color_standing = None
    current_coords = 0, 0
    dirs = collections.deque(((0, 1), (-1, 0), (0, -1), (1, 0)))
    while True:
        try:
            color_painted, rotation = intcode_coro.send(color_standing)
            painted_fields[current_coords] = color_painted
            rotate_val: int = 1 if rotation == 1 else -1
            dirs.rotate(rotate_val)
            current_coords = tuple(map(sum, zip(current_coords, dirs[0])))
            color_standing: int = 1 if painted_fields.get(current_coords) == 1 else 0
        except StopIteration:
            break
    return painted_fields


def draw_message(painted_fields: dict) -> None:
    (min_x, min_y), (max_x, max_y) = (map(func, zip(*painted_fields.keys())) for func in (min, max))
    for y, x in itertools.product(range(max_y, min_y - 1, -1), range(min_x, max_x)):
        sign: str = "#" if painted_fields.get((x, y)) == 1 else "."
        end_line: str = "\n" if x == max_x - 1 else ""
        print(sign, end=end_line)


if __name__ == "__main__":
    painted_starting_black: dict = get_painted_fields(get_program(), initial_input_value=0)
    print("PART1:", len(painted_starting_black))

    painted_starting_white: dict = get_painted_fields(get_program(), initial_input_value=1)
    draw_message(painted_starting_white)

import itertools
from typing import Coroutine, List, Generator, Optional


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


def intcode_computer(program: dict) -> List[int]:
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
    three_output_values: list = []
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
            three_output_values.append(output_value)
            if len(three_output_values) == 3:
                input_value = yield tuple(three_output_values[:2]), three_output_values[2]
                three_output_values.clear()
            index += 2
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


def play_arkonoid(program: dict):
    generated_codes_gen: Coroutine = intcode_computer(program)
    game_map: dict = {}
    score: int = 0
    mv = None
    paddle_coordinates = 22, 22
    blocks_initial_value = None
    while True:
        try:
            (coordinates), tile_id = generated_codes_gen.send(mv)
            if (-1, 0) == coordinates:
                score = tile_id
            else:
                game_map[coordinates] = tile_id
            if tile_id == 4:
                if blocks_initial_value is None:
                    blocks_initial_value = sum(1 for val in game_map.values() if val == 2)
                previous_ball_coordinates = coordinates
                if previous_ball_coordinates[0] > paddle_coordinates[0]:
                    mv = 1
                elif previous_ball_coordinates[0] < paddle_coordinates[0]:
                    mv = -1
                else:
                    mv = 0
            elif tile_id == 3:
                paddle_coordinates = coordinates
        except StopIteration:
            break
    return blocks_initial_value, score


def print_game(game_map: dict):
    icons: dict = {
        0: " ",
        1: "|",
        2: "#",
        3: "_",
        4: "o"
    }
    for (y, x) in itertools.product(range(23 + 1), range(44 + 1)):
        num: int = game_map.get((x, y), 0)
        sign: str = icons[num]
        end_line: str = "\n" if x == 44 else ""
        print(sign, end=end_line)


if __name__ == "__main__":
    part_1, part_2 = play_arkonoid(get_program())
    print("PART1:", part_1)
    print("PART2:", part_2)


# It was not really necessary
# Following the ball step by step (left or right) is enough
# There is no need to calculate next x moves of paddle

# def move_ball(previous_ball_coords: Tuple[int, int],
#               current_ball_coords: Tuple[int, int],
#               initial_paddle_coords: Tuple[int, int]) -> int:
#     max_x = 44
#     paddle_x, paddle_y = initial_paddle_coords
#     previous_ball_x, previous_ball_y = previous_ball_coords
#     move: int = 0
#     ball_x, ball_y = current_ball_coords
#     if ball_y < previous_ball_y:
#         move = 0
#         distance = 0
#     else:
#         moves_left: int = paddle_y - ball_y
#         ball_direction: int = -1 if ball_x < previous_ball_x else 1
#         x, y = ball_x, ball_y
#         for _ in range(moves_left):
#             if x in (1, max_x - 1):
#                 ball_direction *= -1
#             x += 1 * ball_direction
#             y += 1
#             if y == paddle_y:
#                 distance: int = abs(x - paddle_x)
#                 if x > paddle_x:
#                     move = 1
#                 elif x < paddle_x:
#                     move = -1
#                 else:
#                     move = 0
#                 break
#     yield from (move for _ in range(distance))

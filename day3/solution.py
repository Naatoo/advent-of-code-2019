from typing import List, Generator


def get_wires_moves() -> List[Generator[str, None, None]]:
    wires_moves: list = []
    with open("input.txt") as file:
        for line in file.readlines():
            single_wire_move: Generator = (move for move in line.split(","))
            wires_moves.append(single_wire_move)
    return wires_moves


def convert_letter_to_direction(wire_moves: List[Generator]) -> Generator[range, None, None]:
    for move in wire_moves:
        x: int = 0
        y: int = 0
        direction: str = move[0]
        value: int = int(move[1:])
        step: int = 1 if direction in ("R", "U") else -1
        coords_single_move: tuple = (step, 0) if direction in ("R", "L") else (0, step)
        line_move_values: Generator = (coords_single_move for _ in range(1, value + 1))
        yield from line_move_values


def produce_wires_points(wires_paths: list):
    wires_points: List[set, set] = [set(), set()]
    for wire_index, wire in enumerate(wires_paths):
        x = y = 0
        for step_index, (step_x, step_y) in enumerate(convert_letter_to_direction(wire)):
            x += step_x
            y += step_y
            wires_points[wire_index].add((step_index + 1, x, y))
    return wires_points


def get_intersection(wires_points: List[set]) -> set:
    first_wire_without_index, second_wire_without_index = (set(point[1:] for point in wire) for wire in wires_points)
    intersection_points: set = first_wire_without_index.intersection(second_wire_without_index)
    return intersection_points


def count_min_manhattan_distance(wires_points: List[set]) -> int:
    intersection_points: set = get_intersection(wires_points)
    distances: list = [sum(abs(coord) for coord in coordinates) for coordinates in intersection_points]
    min_manhattan_distance: int = min(distances)
    return min_manhattan_distance


def get_closest_distance(wires_paths: list) -> int:
    wires_points: List[set] = produce_wires_points(wires_paths)
    min_dist_int = count_min_manhattan_distance(wires_points)
    return min_dist_int


def find_fewest_steps(wires_paths) -> int:
    wires_points: List[set] = produce_wires_points(wires_paths)
    intersection_points: set = get_intersection(wires_points)
    first_wire, second_wire = [list(points) for points in wires_points]
    wires_without_indexes = [list(point[1:] for point in wire) for wire in wires_points]
    intersection_points_indexes = []
    for point in intersection_points:
        first_wire_point, second_wire_point = (wire_without_index.index(point)
                                               for wire_without_index in wires_without_indexes)
        intersection_points_indexes.append((first_wire_point, second_wire_point))

    steps: list = []
    for first_index, second_index in intersection_points_indexes:
        first_step = first_wire[first_index][0]
        second_step = second_wire[second_index][0]
        total_step = first_step + second_step
        steps.append(total_step)
    fewest_steps: int = min(steps)
    return fewest_steps


if __name__ == "__main__":
    sample_paths: List[List] = [
        ['R8,U5,L5,D3', 'U7,R6,D4,L4'],
        ['R75,D30,R83,U83,L12,D49,R71,U7,L72', 'U62,R66,U55,R34,D71,R55,D58,R83'],
        ['R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51', 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7']
    ]
    for index, sample in enumerate(sample_paths):
        wire_moves: List[Generator] = [(move for move in line.split(",")) for line in sample]
        dist: int = get_closest_distance(wire_moves)
        print(f'PART1 Sample {index + 1} min distance={dist}')

    part_1_dist: int = get_closest_distance(get_wires_moves())
    print(f'PART1={part_1_dist}')

    for index, sample in enumerate(sample_paths):
        wire_moves: List[Generator] = [(move for move in line.split(",")) for line in sample]
        dist: int = find_fewest_steps(wire_moves)
        print(f'PART2 Sample {index + 1} min distance={dist}')

    part_2: int = find_fewest_steps(get_wires_moves())
    print(f'PART2={part_2}')

from collections import defaultdict
from typing import Generator


def read_file(name: str) -> Generator[str, None, None]:
    with open(name) as file:
        yield from file.readlines()


def get_center_and_border(orbits_exp: Generator) -> dict:
    center_borders: defaultdict = defaultdict(list)
    for orb in orbits_exp:
        splitted: list = orb.strip().split(")")
        center_borders[splitted[0]].append(splitted[1])
    return center_borders


def produce_orbits_part1(orbits: dict, start: str) -> dict:
    level: dict = defaultdict(list)
    level[0].append(start)
    index: int = 0
    while not all(val == [] for val in orbits.values()):
        for level_center in level[index]:
            for level_border in (border for center, border in orbits.items() if center == level_center):
                for lvl in level_border:
                    level[index + 1].append(lvl)
            if orbits[level_center]:
                del orbits[level_center]
        index += 1
    return level


def count_orbits(file_name: str) -> int:
    data: dict = get_center_and_border(read_file(file_name))
    mapped_orbits: dict = produce_orbits_part1(data, start="COM")
    number_indirect: int = 0
    for index, centers in mapped_orbits.items():
        number_indirect += index * len(centers)
    return number_indirect


def get_border_and_center(orbits_exp: Generator) -> dict:
    center_borders: dict = {}
    for orb in orbits_exp:
        splitted: list = orb.strip().split(")")
        center_borders[splitted[1]] = splitted[0]
    return center_borders


def produce_orbits_part2(orbits: dict, start: str) -> list:
    parents: list = []
    current_border: str = start
    while True:
        try:
            current_center = orbits[current_border]
        except KeyError:
            break
        parents.append(current_center)
        current_border = current_center
    return parents


def get_path_len(file_name: str) -> int:
    data: dict = get_border_and_center(read_file(file_name))
    parents_you: list = produce_orbits_part2(data, start="YOU")
    parents_san: list = produce_orbits_part2(data, start="SAN")
    for center in parents_you:
        if center in parents_san:
            change_orbit: int = center
            break
    else:
        raise ValueError(f"Common orbit not found for: {parents_san}, {parents_you}")
    path_len = sum(parents.index(change_orbit) for parents in (parents_you, parents_san))
    return path_len


if __name__ == "__main__":
    sample_result_part1: int = count_orbits("sample_input.txt")
    print("SAMPLE RESULT PART 1:", sample_result_part1)

    part_1_result: int = count_orbits("input.txt")
    print("PART1:", part_1_result)

    sample_result_part2: int = get_path_len("sample_input_2.txt")
    print("SAMPLE RESULT PART 2:", sample_result_part2)

    part_2_result: int = get_path_len("input.txt")
    print("PART2:", part_2_result)

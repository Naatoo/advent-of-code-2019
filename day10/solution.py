import collections
import itertools


def read_map(file_name: str) -> dict:
    space_map: dict = {}
    with open(file_name) as file:
        for y, line in enumerate(file.readlines()):
            for x, sign in enumerate(line):
                space_map[(x, y)] = sign
    return space_map


def find_best_asteroid(space_map: dict):
    final_coords = None
    final_value = 0
    for (x, y), obj in space_map.items():
        if obj == "#":
            coeffs: dict = get_coeffs(space_map, x, y)
            quantity = sum(len(val) for val in coeffs.values())
            if quantity > final_value:
                final_value = quantity
                final_coords = x, y
    return final_coords, final_value


def get_coeffs(space_map: dict, base_x: int, base_y: int):
    categories: tuple = "above_right", "above_left", "below", "horizontal", "vertical_up"
    coeffs: dict = {cat: collections.defaultdict(list) for cat in categories}
    for (x, y), obj in space_map.items():
        if obj == "#":
            x_offset: int = x - base_x
            y_offset: int = y - base_y
            if y_offset == 0:
                pos = "horizontal"
                if x_offset > 0:
                    div: float = 1
                elif x_offset < 0:
                    div: float = -1
                else:
                    continue
            else:
                div: float = x_offset / y_offset
                if y > base_y:
                    pos: str = "below"
                elif x_offset > 0:
                    pos: str = "above_right"
                elif x_offset < 0:
                    pos: str = "above_left"
                else:
                    pos: str = "vertical_up"
            coeffs[pos][div].append((x, y))
    return coeffs


def distance_between_points(base_x: int, base_y: int, x: int, y: int) -> float:
    distance: float = ((x - base_x) ** 2 + (-y + base_y) ** 2) ** (1 / 2)
    return distance


def get_200th_destroyed_asteroid(space_map: dict, base_x: int, base_y: int) -> tuple:
    raw_coeffs = get_coeffs(space_map, base_x, base_y)
    sorted_coeffs = {cat: collections.OrderedDict(sorted(raw_coeffs[cat].items(), key=lambda t: -t[0]))
                     for cat in ("above_right", "below", "above_left")}
    order = raw_coeffs["vertical_up"],\
            sorted_coeffs["above_right"],\
            {1: raw_coeffs["horizontal"][1]}, \
            sorted_coeffs["below"],\
            {1: raw_coeffs["horizontal"][-1]},\
            sorted_coeffs["above_left"]
    index: int = 1
    for part in itertools.cycle(itertools.chain(order)):
        if index == 200:
            break
        for coeff, coords in part.items():
            if coords:
                points_distance: list = [distance_between_points(base_x, base_y, x, y) for x, y in coords]
                nearest_asteroid_index: int = points_distance.index(min(points_distance))
                if index == 200:
                    asteroid_200_coords: tuple = coords[nearest_asteroid_index]
                    break
                coords.pop(nearest_asteroid_index)
                index += 1
    return asteroid_200_coords


if __name__ == "__main__":
    sp_map: dict = read_map("input.txt")
    part_1_coords, part_1_value = find_best_asteroid(sp_map)
    print("PART1:", part_1_value)

    part_2_coords: tuple = get_200th_destroyed_asteroid(sp_map, *part_1_coords)
    part_2_res: int = part_2_coords[0] * 100 + part_2_coords[1]
    print("PART2:", part_2_res)

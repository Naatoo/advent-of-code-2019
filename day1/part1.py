from typing import Generator, Callable


def get_mass_from_file():
    with open("input.txt") as file:
        yield from file.readlines()


def calculate_single_fuel(mass: int) -> int:
    fuel_quantity: int = mass // 3 - 2
    return fuel_quantity


def calculate_single_module_with_fuel(initial_fuel: int) -> int:
    module_mass: int = calculate_single_fuel(initial_fuel)
    left_mass: int = module_mass
    while calculate_single_fuel(left_mass) > 0:
        left_mass = calculate_single_fuel(left_mass)
        module_mass += left_mass
    return module_mass


def count_total(calculator: Callable[[int], int]) -> int:
    fuels: Generator = (calculator(int(mass)) for mass in get_mass_from_file())
    total: int = sum(fuels)
    return total


if __name__ == "__main__":
    sample: tuple = 12, 14, 1969, 100756
    sample_res_part1: list = [calculate_single_fuel(mass) for mass in sample]
    print("SAMPLE PART 1:", sample_res_part1)

    total_fuel_part1: int = count_total(calculate_single_fuel)
    print("PART 1:", total_fuel_part1)

    sample_res_part2: list = [calculate_single_module_with_fuel(mass) for mass in sample]
    print("SAMPLE PART 2:", sample_res_part2)

    total_fuel_part2: int = count_total(calculate_single_module_with_fuel)
    print("PART 2:", total_fuel_part2)

from collections import Counter
from typing import Callable, Generator


def get_adjacent_digits_identical(num: str) -> list:
    adjacent_digit: list = [num[index + 1] for index in range(5) if num[index] == num[index + 1]]
    return adjacent_digit


def are_digits_increasing(num: str) -> bool:
    status: bool = all(num[index - 1] <= num[index] for index, _ in enumerate(num) if index > 0)
    return status


def part_2_condition(num: str):
    adjacents: list = get_adjacent_digits_identical(num)
    quantity: Counter = Counter(num)
    status: bool = True if any(quantity[adj] == 2 for adj in adjacents) else False
    return status


def assert_conditions_and_get_quantity(start: int, stop: int, cond_1: Callable, cond_2: Callable) -> int:
    passwords: Generator = (num for num in range(start, stop + 1) if cond_1(str(num)) and cond_2(str(num)))
    quantity: int = len(list(passwords))
    return quantity


if __name__ == "__main__":
    start: int = 248345
    stop: int = 746315
    part_1 = assert_conditions_and_get_quantity(start, stop, get_adjacent_digits_identical, are_digits_increasing)
    print(f"PART 1: {part_1}")

    part_2 = assert_conditions_and_get_quantity(start, stop, part_2_condition, are_digits_increasing)
    print(f"PART 2: {part_2}")



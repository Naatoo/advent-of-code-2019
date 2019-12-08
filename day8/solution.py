import collections
import itertools
from typing import Generator


def read_image_data() -> Generator[int, None, None]:
    with open("input.txt") as file:
        yield from (int(num) for num in file.read())


def part_1(num_gen: Generator, width: int, height: int):
    fewest_0_val_counter: collections.Counter = {0: 100}
    while True:
        try:
            occurrences = collections.Counter(next(num_gen) for _ in range(width * height))
        except RuntimeError:
            break
        if occurrences[0] < fewest_0_val_counter[0]:
            fewest_0_val_counter = occurrences
    result = fewest_0_val_counter[1] * fewest_0_val_counter[2]
    return result


def part_2_decode_image(num_gen: Generator, width: int, height: int) -> dict:
    layer_size: int = width * height
    decoded_image: dict = {index: 2 for index in range(layer_size)}
    for index, num in zip(itertools.cycle(range(layer_size)), num_gen):
        if decoded_image.get(index) not in (0, 1):
            decoded_image[index] = num
    return decoded_image


def message_printer(decoded_image: dict, width_img: int) -> None:
    for index, num in decoded_image.items():
        end = "" if (index + 1) % width_img != 0 else "\n"
        print(num if num == 1 else ".", end=end)


if __name__ == "__main__":
    width: int = 25
    height: int = 6

    part_1_res = part_1(read_image_data(), width, height)
    print("PART1:", part_1_res)

    part_2_decoded_image = part_2_decode_image(read_image_data(), width, height)
    print("PART2:")
    message_printer(part_2_decoded_image, width)



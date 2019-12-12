from __future__ import annotations
import copy
import math
import itertools
from typing import Tuple, Generator, List


def read_moons() -> Generator[List[int], None, None]:
    with open("input.txt") as file:
        for line in file.readlines():
            _, x, _, y, _, z = line.replace("=", " ").replace(",", " ").replace(">", " ").split()
            yield list(map(int, (x, y, z)))


class Moon:
    def __init__(self, coordinates: List[int], name) -> None:
        self.coordinates: list = coordinates
        self.velocity: list = [0, 0, 0]
        self.name: str = name

    def update_gravity(self, other: Moon) -> None:
        for index, (coord, coord_other) in enumerate(zip(self.coordinates, other.coordinates)):
            if coord == coord_other:
                val: int = 0
            elif coord < coord_other:
                val: int = 1
            else:
                val: int = -1
            self.velocity[index] += val

    def move(self) -> None:
        for index, vel in enumerate(self.velocity):
            self.coordinates[index] += vel

    @property
    def potential_energy(self) -> int:
        energy: int = sum(map(abs, self.coordinates))
        return energy

    @property
    def kinetic_energy(self) -> int:
        energy: int = sum(map(abs, self.velocity))
        return energy

    @property
    def total_energy(self) -> int:
        total_energy: int = self.potential_energy * self.kinetic_energy
        return total_energy

    def identical_coord_and_velocity(self, other: Moon, index: int):
        res: bool = True if self.coordinates[index] == other.coordinates[index] \
                            and self.velocity[index] == other.velocity[index] else False
        return res


def lowest_common_multiple(a: int, b: int) -> int:
    lcm: int = a * b // math.gcd(a, b)
    return lcm


def simulate_moons(initial_coordinates: Generator[List[int], None, None], steps: int):
    moon_names: Tuple[str, ...] = "Io", "Europa", "Ganymede", "Callisto"
    moons: List[Moon] = list(Moon(coordinates, name) for coordinates, name in zip(initial_coordinates, moon_names))
    initial_moons = copy.deepcopy(moons)
    interactions = list(itertools.permutations(moons, 2))
    x_index, y_index, z_index = 0, 0, 0
    for total_index in itertools.count():
        if total_index == steps - 1:
            total_energy: int = sum(m.total_energy for m in moons)
        if all((moon.identical_coord_and_velocity(initial_moon, 0) for moon, initial_moon in zip(moons, initial_moons))):
            if not x_index:
                x_index = total_index
        if all((moon.identical_coord_and_velocity(initial_moon, 1) for moon, initial_moon in zip(moons, initial_moons))):
            if not x_index:
                y_index = total_index
        if all((moon.identical_coord_and_velocity(initial_moon, 2) for moon, initial_moon in zip(moons, initial_moons))):
            if not x_index:
                z_index = total_index
        if x_index and y_index and z_index:
            step_index_identical = lowest_common_multiple(x_index, lowest_common_multiple(y_index, z_index))
            break
        for inter in interactions:
            inter[0].update_gravity(inter[1])
        for m in moons:
            m.move()
    return total_energy, step_index_identical


if __name__ == "__main__":
    part_1, part_2 = simulate_moons(read_moons(), steps=1000)
    print("PART1:", part_1)
    print("PART2:", part_2)

from itertools import product


class Vector:
    def __init__(self, data):
        self._vector = data

    def __add__(self, other):
        return Vector([a + b for a, b in zip(self._vector, other._vector)])

    def __mul__(self, other):
        return Vector([other * a for a in self._vector])
    def __rmul__(self, other):
        return self * other

    def __sub__(self, other):
        return self + (other * -1)

    def __getitem__(self, item):
        return self._vector[item]

    def __repr__(self):
        return "<" + ", ".join([str(a) for a in self._vector]) + ">"

    def __eq__(self, other):
        for a,b in zip(self._vector, other._vector):
            if a != b:
                return False
        return  True

    def __hash__(self):
        out = ""
        for a in self._vector:
            out += str(a)
            out += "0"
        return int(out)

    def to_tuple(self):
        return tuple(a for a in self._vector)
    def to_list(self):
        return [a for a in self._vector]


def parse(filepath):
    with open(filepath, "r") as file:
        return [line[:-1] for line in file.readlines()]

def in_grid(coords, dimensions):
    return ((0 <= coords[0] < dimensions[0]) and (0 <= coords[1] < dimensions[1]))

grid = parse("input")
#grid = parse("test")

dimensions = len(grid), len(grid[0])

frequencies = {}
for i, line in enumerate(grid):
    for k, char in enumerate(line):
        if char != ".":
            try:
                frequencies[char].append((i, k))
            except KeyError:
                frequencies[char] = [(i, k)]

antinodes = set()
for frequency, locations in frequencies.items():
    combos = list(product(locations, repeat=2))
    combos_ = []
    for combo in combos:
        if (combo[1], combo[0]) not in combos_ and combo[0] != combo[1]:
            combos_.append(combo)
    for combo in combos_:
        a = Vector(combo[0])
        b = Vector(combo[1])

        diff = b - a
        antinode = b
        while in_grid(antinode, dimensions):
            antinodes.update({antinode})
            antinode = antinode + diff
        antinode = a
        while in_grid(antinode, dimensions):
            antinodes.update({antinode})
            antinode = antinode - diff

print(len(antinodes))
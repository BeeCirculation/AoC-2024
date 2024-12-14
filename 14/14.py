import re

class Vector:
    def __init__(self, data):
        self.data = list(data)
        self.dimension = len(data)

    def __add__(self, other: "Vector"):
        if isinstance(other, int) or isinstance(other, float):
            return Vector([a + other for a in self.data])

        if self.dimension != other.dimension:
            raise ValueError

        return Vector([a + b for a, b in zip(self.data, other.data)])

    def __mul__(self, other):
        if not isinstance(other, int):
            raise ValueError

        return Vector([a * other for a in self.data])

    def __mod__(self, other):
        if isinstance(other, int):
            other = Vector([other] * self.dimension)

        if other.dimension != self.dimension:
            raise ValueError("None conformable Vector objects")

        return Vector([a % b for a,b in zip(self, other)])

    def __iter__(self):
        self.index = 0
        return self
    def __next__(self):
        if self.index >= self.dimension:
            raise StopIteration

        output = self[self.index]
        self.index += 1
        return output

    def __getitem__(self, item):
        return self.data[item]

    def __eq__(self, other):
        if self.dimension != other.dimension:
            return False
        for a,b in zip(self.data, other.data):
            if a != b:
                return False
        return True

    def __str__(self):
        return str(self.data).replace("[", "<").replace("]", ">")


def parse(fp):
    with open(fp, "r") as file:
        text = file.readlines()
        robots = [{"start": Vector([int(a) for a in re.search(r"p=(-?\d+),(-?\d+)", line).groups()]),
                   "velocity": Vector([int(a) for a in re.search(r"v=(-?\d+),(-?\d+)", line).groups()])} for line in text]
    return robots


def calculate_position(start_pos: Vector, velocity: Vector, time: float | int) -> Vector:
    return start_pos + (velocity * time)


positions = []
dimensions = Vector([101, 103])
#dimensions = Vector([11, 7])

grid = [[0 for _ in range(dimensions[0])].copy() for _ in range(dimensions[1])]

robots = parse("input")
#robots = parse("test")

for robot in robots:
    # Find the positions of robots in 100 seconds
    positions.append(calculate_position(robot["start"], robot["velocity"], 100) % dimensions)

# Find the number of robots at a position in a grid
for position in positions:
    grid[position[1]][position[0]] += 1

# Split into quadrants
half1 = grid[:dimensions[1] // 2]
half2 = grid[dimensions[1] // 2 + 1:]

q1 = [line[:dimensions[0] // 2] for line in half1]
q2 = [line[dimensions[0] // 2 + 1:] for line in half1]
q3 = [line[:dimensions[0] // 2] for line in half2]
q4 = [line[dimensions[0] // 2 + 1:] for line in half2]

# calculate safety score
safety_score = 1
quads = [q1,q2,q3,q4]
for q in quads:
    score = 0
    for line in q:
        score += sum(line)
    safety_score *= score

print(safety_score)
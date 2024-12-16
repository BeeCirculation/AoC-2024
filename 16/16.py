import math

from MyVector import Vector, rotate2D

def parse(fp):
    with open(fp, "r") as file:
        return [list(line) for line in file.read().split("\n")]


def find_start_end(grid):
    start, end = None, None

    for i, line in enumerate(grid):
        try:
            start = line.index("S"), i
            end = line.index("E"), i
        except IndexError:
            pass

    if start is None or end is None:
        raise IndexError("Couldnt find start or end")

    return Vector(start), Vector(end)

class Reindeer:
    def __init__(self, pos: Vector, direction:Vector):
        self.pos = pos
        self.direction = direction

    @property
    def right_dir(self):
        return rotate2D(self.direction, -0.5 * math.pi)

    @property
    def left_dir(self):
        return rotate2D(self.direction, 0.5 * math.pi)

    def turn_right(self):
        self.direction.rotate2D(-0.5 * math.pi)

    def turn_left(self):
        self.direction.rotate2D(0.5 * math.pi)

def get_score(pos: Vector):
    directions = {Vector.RIGHT, Vector.LEFT, Vector.UP, Vector.DOWN}
    directions = {direction.change_dimension(2) for direction in directions}

    




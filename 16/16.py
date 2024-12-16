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


directions = {Vector.UP, Vector.DOWN, Vector.RIGHT, Vector.LEFT}
directions = [direction.change_dimension(2) for direction in directions]

def find_adjacent(pos: Vector, grid: list[list[str]]) -> list[Vector]:
    if grid[pos.y][pos.x] != ".":
        raise ValueError

    adj = []
    for direction in directions:
        new_pos = pos + direction
        if grid[new_pos.y][new_pos.x] == ".":
            adj.append(new_pos)

    return adj


maze = parse("test")
start, end = find_start_end(maze)

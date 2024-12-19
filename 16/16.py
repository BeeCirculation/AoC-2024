from MyVector import Vector
import MyVector
from MyGraph import dijkstra_all

def parse(fp):
    with open(fp, "r") as file:
        return [list(line) for line in file.read().split("\n")]


def find_start_end(grid):
    start, end = None, None

    for i, line in enumerate(grid):
        try:
            start = i, line.index("S")
        except ValueError:
            pass
        try:
            end = i, line.index("E")
        except ValueError:
            pass

    if start is None or end is None:
        raise ValueError("Couldnt find start or end")

    return Vector(start), Vector(end)


directions = [Vector([0, 1]), Vector([1, 0]), Vector([0, -1]), Vector([-1, 0])]


maze = parse("input")
'''
maze = ["#######",
        "#....E#",
        "##.#.##",
        "#S....#",
        "#######"]
'''

start, end = find_start_end(maze)

def adj(vertex):
    coord, direction = vertex
    yield (coord, (direction + 1) % 4), 1000
    yield (coord, (direction - 1) % 4), 1000
    y, x = coord + directions[direction]
    if maze[int(y)][int(x)] != "#":
        yield (coord + directions[direction], direction), 1

distance, paths = dijkstra_all((start, 0), adj, None, lambda c, v: c[0] == end)
paths = [[pos for pos, dirc in path] for path in paths]
out = set()
for path in paths:
    out.update(set(path))
print(len(out))
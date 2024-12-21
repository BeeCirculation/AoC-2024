import MyVector
from MyVector import Vector, Grid, UP, DOWN, LEFT, RIGHT
from MyGraph import dijkstra, get_branches
import sys


dimension = 7


def q2g(x: Vector):
    a1, b1, a2, b2 = dimension - 1, 0, 0, dimension - 1
    range1 = b1 - a1
    range2 = b2 - a2
    factor = range2 / range1

    def _map(val):
        return (val - a1) * factor + a2

    return Vector(x.x, _map(x.y))


def g2q(x: Vector):
    a1, b1, a2, b2 = dimension - 1, 0, 0, dimension - 1
    range1 = b1 - a1
    range2 = b2 - a2
    factor = range2 / range1

    def _map(val):
        return (val - a1) * factor + a2

    return Vector(x.x, _map(x.y))


def parse(fp):
    with open(fp, "r") as file:
        return [q2g(Vector(line.split(","))) for line in file.readlines()]


grid = Grid(dimension, dimension, ".")
bytes = parse("test")
for byte in bytes[:12]:
    grid[byte] = "#"


def adj2(vertex, distances):
    directions = [UP, DOWN, LEFT, RIGHT]
    directions = [d.change_dimension(2) for d in directions]
    for direction in directions:
        new_pos = vertex + direction
        if grid.in_grid(new_pos) and (new_pos not in bytes[:distances[vertex][0]]):
            yield new_pos


def adj(vertex, distances):
    directions: list[Vector] = [UP, DOWN, LEFT, RIGHT]
    directions = [d.change_dimension(2) for d in directions]
    for direction in directions:
        new_pos = vertex + direction
        if grid.in_grid(new_pos) and grid[new_pos] != "#":
            yield new_pos, 1


def vis(current: Vector, dists, visited, q):
    for _, a in q:
        grid[a] = "•"

    for vert in visited:
        grid[vert] = "○"

    for vert in get_branches(current, lambda n: [dists[n][1]] if dists[n][1] else None)[0]:
        grid[vert] = "●"

    grid[current] = "◈"

    sys.stdout.write(f"\033[{grid.height + 1}A") # Move up
    sys.stdout.write(str(grid))
    #input()

for _ in range(grid.height + 1):
    print()
steps, path = dijkstra(g2q(Vector(0,0)), adj, g2q(Vector(dimension - 1, dimension - 1)), visualiser=vis)
print(steps)

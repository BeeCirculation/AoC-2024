from copy import deepcopy

import MyVector
from MyVector import Vector, Grid, UP, DOWN, LEFT, RIGHT
from MyGraph import dijkstra, get_branches
import sys


dimension = 71


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


wall_char = "▦"
bytes = parse("input")
grid = Grid(dimension, dimension, ".")


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
        if grid.in_grid(new_pos) and grid[new_pos] != wall_char:
            yield new_pos, 1


def vis(current: Vector, dists, visited, q):
    for _, a in q:
        grid[a] = "•"

    for vert in visited:
        grid[vert] = "○"

    verts = set()
    for branch in get_branches(current, lambda n: [dists[n][1]] if dists[n][1] else None):
        verts.update(set(branch))

    for vert in verts:
        grid[vert] = "●"

    grid[current] = "◈"

    sys.stdout.write(f"\033[{grid.height}A") # Move up
    sys.stdout.write(str(grid))
    #input("\033[1A")


print(grid, end="")
input("\033[1A")
grid_base = deepcopy(grid)

i = 1
steps = 0
while i:
    print(i, str(steps))
    print(" " * 100, end="\r") # clear line
    try:
        i = int(input("> "))
    except ValueError:
        break
    print("", end="\033[2A")
    print(" " * 100, end="\r")

    for k in range(i):
        byte = bytes[k]
        grid[byte] = wall_char

    steps, path = dijkstra(source=g2q(Vector(0,0)),
                           get_adjacent=adj,
                           target=g2q(Vector(dimension - 1, dimension - 1)),
                           visualiser=vis)
    grid = deepcopy(grid_base)
print(g2q(bytes[i - 1]))

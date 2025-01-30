from functools import cache
from itertools import permutations

from MyVector import Vector

numeric_keypad = { 0: Vector(1, 0),
                   "A": Vector(2,0),
                   1: Vector(0,1),
                   2: Vector(1,1),
                   3: Vector(2,1),
                   4: Vector(0, 2),
                   5: Vector(1,2),
                   6: Vector(2,2),
                   7: Vector(0,3),
                   8: Vector(1,3),
                   9: Vector(2,3)
                   }

directional_keypad = { "<": Vector(0,0),
                       "v": Vector(1,0),
                       ">": Vector(2, 0),
                       "^": Vector(1,1),
                       "A": Vector(2, 1)
                       }

directions = { "<": Vector(-1, 0),
               "v": Vector(0, -1),
               ">": Vector(1, 0),
               "^": Vector(0, 1)}

def get_paths(start, end, keypad):
    keypad = directional_keypad if keypad else numeric_keypad

    # Generate all the different paths from one button to the next
    cursor = keypad[start].__copy__()
    destination = keypad[end].__copy__()
    distances = destination - cursor
    moves = ""
    if distances.x > 0:
        moves += ">" * int(distances.x)
    else:
        moves += "<" * -int(distances.x)
    if distances.y > 0:
        moves += "^" * int(distances.y)
    else:
        moves += "v" * -int(distances.y)
    moves = list(set(["".join(move) + "A" for move in permutations(moves)]))
    valid_moves = []

    # Validate paths that dont cross over an empty space
    for move in moves:
        location = cursor.__copy__()
        valid = True
        for step in move[:-1]:
            location += directions[step]
            if location not in keypad.values():
                valid = False
                break
        if valid:
            valid_moves.append(move)

    return valid_moves

@cache
def get_cost(start, end, keypad, depth=0):
    paths = get_paths(start, end, keypad)

    if depth <= 1:
        return len(paths[0])

    cheapest = 1_000_000_000_000_000_000
    for path in paths:
        path = "A" + path
        cost = 0
        for i in range(len(path) - 1):
            a = path[i]
            b = path[i+1]
            subcost = get_cost(a, b, True, depth - 1)
            cost += subcost
        cheapest = cost if cost < cheapest else cheapest

    return cheapest

def complexity(code, depth):
    cost = 0

    code = ["A"] + [int(c) for c in code[:-1]] + [code[-1]]

    for i in range(len(code) - 1):
        a, b = code[i], code[i + 1]
        cost += get_cost(a, b, False, depth)

    code = "".join([str(x) for x in code[1:-1]])

    return int("".join(code)) * cost


def total_complexity(codes, depth):
    return sum([complexity(code, depth) for code in codes])


codes = [ "029A",
          "980A",
          "179A",
          "456A",
          "379A"
          ]


with open("input", "r") as file:
    codes = file.readlines()

codes = [code.replace("\n", "") for code in codes]

print(total_complexity(codes, 26))

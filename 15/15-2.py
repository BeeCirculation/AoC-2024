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

    def __iadd__(self, other):
        self.data = (self + other).data
        return self

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector([a - other for a in self.data])

        if self.dimension != other.dimension:
            raise ValueError

        return Vector([a - b for a, b in zip(self.data, other.data)])

    def __isub__(self, other):
        self.data = (self - other).data
        return self

    def __rsub__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector([other - a for a in self.data])
        else:
            raise TypeError

    def __mul__(self, other):
        if not isinstance(other, int) and not isinstance(other, float):
            raise TypeError

        return Vector([a * other for a in self.data])

    def __imul__(self, other):
        self.data = (self * other).data
        return self

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector([a / other for a in self])
        else:
            raise TypeError

    def __itruediv__(self, other):
        self.data = (self / other).data
        return self

    def __rtruediv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector([other / a for a in self])
        else:
            raise TypeError

    def __floordiv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector([a // other for a in self])
        else:
            raise TypeError

    def __ifloordiv__(self, other):
        self.data = (self // other).data
        return self

    def __rfloordiv__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Vector([other // a for a in self])
        else:
            raise TypeError

    def __mod__(self, other):
        if isinstance(other, int):
            other = Vector([other] * self.dimension)

        if other.dimension != self.dimension:
            raise ValueError("None conformable Vector objects")

        return Vector([a % b for a, b in zip(self, other)])

    def __imod__(self, other):
        self.data = (self % other).data
        return self

    def __rmod__(self, other):
        if isinstance(other, int):
            return Vector([other % a for a in self])
        else:
            raise TypeError

    def __round__(self, n=None):
        return Vector([round(a, n) for a in self])

    def __ceil__(self):
        return Vector([a.__ceil__() for a in self])

    def __floor__(self):
        return Vector([a.__floor__() for a in self])

    def __len__(self):
        return self.dimension

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
        for a, b in zip(self.data, other.data):
            if a != b:
                return False
        return True

    def __str__(self):
        return str(self.data).replace("[", "<").replace("]", ">")


def parse(fp):
    with open(fp, "r") as file:
        grid, moves = file.read().split("\n\n")

    # Doubling the width of the grid for part 2
    grid = (grid
            .replace("#", "##")
            .replace("O", "[]")
            .replace(".", "..")
            .replace("@", "@."))

    grid = [list(line) for line in grid.split("\n")]
    moves = moves.replace("\n", "")

    return grid, moves


directions = {"^": Vector([-1, 0]),
              ">": Vector([0, 1]),
              "v": Vector([1, 0]),
              "<": Vector([0, -1])}


def find_robot(grid: list[list[str]]):
    for i, line in enumerate(grid):
        try:
            return Vector([i, line.index("@")])
        except ValueError:
            pass
    raise ValueError("Couldnt find @ in grid")


def check_move(grid, pos: Vector, direction: Vector):
    """
    Will check to see if a move of an object and all objects in front of it if possible

    Args:
        grid (list[list[str]]): The grid in which the objects exist
        pos (Vector): The position in the grid being moved from
        direction (Vector): The direction being moved in

    Returns (bool):
        True: If the move was possible.
        False: If the move was not possible.

    """
    new_coord = pos + direction
    try:
        new_space = grid[new_coord[0]][new_coord[1]]
    except IndexError:
        return False

    if new_space == "#":
        return False

    if new_space == ".":
        # grid[new_coord[0]][new_coord[1]] = grid[pos[0]][pos[1]]
        # grid[pos[0]][pos[1]] = "."
        return True

    if new_space == "[":
        # We must check if both the objects in front of this side are moveable
        # AND the objects in front of it's other side
        if not check_move(grid, new_coord, direction):
            return False
        if (direction != directions["<"]
                and direction != directions[">"]
                and not check_move(grid, new_coord + directions[">"], direction)):
            return False

        # grid[new_coord[0]][new_coord[1]] = grid[pos[0]][pos[1]]
        # grid[pos[0]][pos[1]] = "."
        return True
    if new_space == "]":
        if not check_move(grid, new_coord, direction):
            return False
        if (direction != directions["<"]
                and direction != directions[">"]
                and not check_move(grid, new_coord + directions["<"], direction)):
            return False

        # grid[new_coord[0]][new_coord[1]] = grid[pos[0]][pos[1]]
        # grid[pos[0]][pos[1]] = "."
        return True


def do_move(grid, pos: Vector, direction: Vector):
    """
    Will check to see if a move of an object and all objects in front of it if possible

    Args:
        grid (list[list[str]]): The grid in which the objects exist
        pos (Vector): The position in the grid being moved from
        direction (Vector): The direction being moved in

    Returns (bool):
        True: If the move was possible.
        False: If the move was not possible.

    """
    new_coord = pos + direction
    try:
        new_space = grid[new_coord[0]][new_coord[1]]
    except IndexError:
        return False

    if new_space == "#":
        return False

    if new_space == ".":
        grid[new_coord[0]][new_coord[1]] = grid[pos[0]][pos[1]]
        grid[pos[0]][pos[1]] = "."
        return True

    if new_space == "[":
        # We must move everything in front AND the objects to the right
        do_move(grid, new_coord, direction)
        if (direction != directions["<"]
            and direction != directions[">"]):
            do_move(grid, new_coord + directions[">"], direction)

        grid[new_coord[0]][new_coord[1]] = grid[pos[0]][pos[1]]
        grid[pos[0]][pos[1]] = "."
        return True
    if new_space == "]":
        # We must move everything in front AND the objects to the left
        do_move(grid, new_coord, direction)
        if (direction != directions["<"]
            and direction != directions[">"]):
            do_move(grid, new_coord + directions["<"], direction)

        grid[new_coord[0]][new_coord[1]] = grid[pos[0]][pos[1]]
        grid[pos[0]][pos[1]] = "."
        return True



def find_all(line: str, substr: str):
    if line == "" or substr == "":
        raise ValueError

    indices = []
    index = -len(substr)
    while index is not None:
        index = line.find(substr, index + len(substr))
        if index == -1:
            break
        indices.append(index)
    return indices


def find_boxes(grid):
    locations = []
    for i, line in enumerate(grid):
        line = "".join(line)
        horiz = find_all(line, "O")
        for num in horiz:
            locations.append(i * 100 + num)
    return locations


def main():
    warehouse, moves = parse("test_big")
    robot = find_robot(warehouse)

    print("\n".join(["".join(line) for line in warehouse]))
    print()
    for move in moves:
        direction = directions[move]
        print(move)

        if check_move(warehouse, robot, direction):
            do_move(warehouse, robot, direction)
            robot += direction
        print("\n".join(["".join(line) for line in warehouse]))
        print()

    print(sum(find_boxes(warehouse)))


main()
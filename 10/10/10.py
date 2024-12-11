def parse(fp):
    with open(fp, "r") as file:
        return [line[:-1] for line in file.readlines()]


def get_score(grid: list[str], position: tuple[int, int], unique=False):
    """
    Finds the score of a trailhead. The score of a trailhead is the number of maximum positions that can be reached
    from it by following a path of contiguous, ascending numbers

    Args:
         grid (list[str]): The elevation map containing the height information of each point
         position (tuple[int, int]): The position in the grid to consider
         unique (bool): Whether the function considers trails that reach same maximum position as unique
    Returns:
         set[tuple[int, int]]: A set of all maximum positions if unique is True
         list[tuple[int, int]]: A list of all maximum positions if unique is False
    """
    directions = [(1,0), (0,1), (-1,0), (0,-1)]
    MAX = 9
    x, y = position
    start = int(grid[x][y])

    if start == MAX:
        return {(x, y)} if unique else [(x, y)]

    # For every direction form a point, its score is the sum of all scores of its surrounding points
    # If a point doesn't reach the maximum value, it's score is 0
    score = set() if not unique else []
    for d in directions:
        next_x, next_y = x + d[0], y + d[1]
        if 0 <= next_x < len(grid) and 0 <= next_y < len(grid[0]):
            next = int(grid[next_x][next_y])
            if next == start + 1:
                if not unique:
                    score.update(get_score(grid, (next_x, next_y), unique))
                else:
                    score.extend(get_score(grid, (next_x, next_y), unique))

    return score



map = parse("input")
#map = parse("test")

sum_ = 0
for i, line in enumerate(map):
    for k, char in enumerate(line):
        if char == "0":
            score_ = len(get_score(map, (i, k), False))
            print(score_)
            sum_ += score_
print(sum_)

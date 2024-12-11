def parse(fp):
    with open(fp, "r") as file:
        return [line[:-1] for line in file.readlines()]


def get_score(grid, position, unique=True):
    directions = [(1,0), (0,1), (-1,0), (0,-1)]
    MAX = 9
    x, y = position
    start = int(grid[x][y])

    if start == MAX:
        return {(x, y)}

    score = set() if unique else []
    for d in directions:
        next_x, next_y = x + d[0], y + d[1]
        if 0 <= next_x < len(grid) and 0 <= next_y < len(grid[0]):
            next = int(grid[next_x][next_y])
            if next == start + 1:
                if unique:
                    score.update(get_score(grid, (next_x, next_y), unique))
                else:
                    score.extend(get_score(grid, (next_x, next_y), unique))


    return score



map = parse("input")
#map = parse("test")

sum = 0
for i, line in enumerate(map):
    for k, char in enumerate(line):
        if char == "0":
            score = len(get_score(map, (i, k), False))
            print(score)
            sum += score
print(sum)

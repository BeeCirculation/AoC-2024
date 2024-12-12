with open("input", "r") as file:
    stones = [int(stone) for stone in file.readline().split(" ")]


def rule1(line, index):
    new_line = line.copy()
    new_line[index] = 1
    return new_line, index


def rule2(line, index):
    left = line[:index]
    right = line[index + 1:]
    nums = split_num(line[index])
    return left + [nums[0], nums[1]] + right, index + 1


def rule3(line, index):
    new_line = line.copy()
    num = new_line[index]
    new_line[index] = num * 2024
    return new_line, index


def num_digits(num):
    return len(str(num))


def split_num(num):
    num_str = str(num)
    num_len = len(num_str)
    return int(num_str[0:num_len // 2]), int(num_str[num_len // 2:])

# A list of tuples of each rule and their conditions
rules = [((lambda x: x == 0), rule1),
         ((lambda x: num_digits(x) % 2 == 0), rule2),
         (lambda x: True, rule3)]

#stones = [125, 17]

def Cache(func):
    _cache = {}

    def wrapper(*args):
        if args in _cache:
            return _cache[args]

        _cache[args] = func(*args)
        return _cache[args]
    return wrapper

@Cache
def count(stone, steps):
    if steps == 0:
        return 1
    if stone == 0:
        return count(1, steps - 1)
    string = str(stone)
    length = len(string)
    if length % 2 == 0:
        return count(int(string[: length // 2]), steps - 1) + count(int(string[length // 2:]), steps - 1)
    return count(stone * 2024, steps - 1)


print(sum([count(stone, 75) for stone in stones]))
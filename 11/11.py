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

for k in range(75):
    i = 0
    # Each while loop is one blink
    while i < len(stones):
        print(k, f"{i} / {len(stones)}")
        for condition, rule in rules:
            if condition(stones[i]):
                stones, i = rule(stones, i)
                break
        i += 1
print(stones)
print(len(stones))
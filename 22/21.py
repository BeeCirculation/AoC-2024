def mix_prune(secret, value):
    secret =  secret ^ value
    return secret % 16777216


def find_next(secret):
    value = secret << 6    # secret * 64
    secret = mix_prune(secret, value)
    value = secret >> 5    # secret // 32
    secret = mix_prune(secret, value)
    value = secret << 11    # secret * 2048
    secret = mix_prune(secret, value)
    return secret


def parse(fp):
    with open(fp, "r") as file:
        nums = file.readlines()
    return [int(num) for num in nums]


buyers = [1, 10, 100, 2024]
buyers = parse("input")

last_nums = []
for buyer in buyers:
    number = buyer
    for _ in range(2000):
        number = find_next(number)
    last_nums.append(number)

print(sum(last_nums))


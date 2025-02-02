import sys

def progress_bar(progress, total, length=40):
    percent = progress / total
    bar = "#" * int(percent * length) + "-" * (length - int(percent * length))
    sys.stdout.write(f"\r[{bar}] {percent*100:.2f}%")
    sys.stdout.flush()


def mix_prune(secret, value):
    secret =  secret ^ value
    return secret % 16777216


def find_next(secret):
    value = secret << 6    # secret * 64
    secret = mix_prune(secret, value)
    value = secret >> 5    # secret // 32
    secret = mix_prune(secret, value)
    value = secret << 11   # secret * 2048
    secret = mix_prune(secret, value)
    return secret


def parse(fp):
    with open(fp, "r") as file:
        nums = file.readlines()
    return [int(num) for num in nums]


buyers = [1, 10, 100, 2024]
buyers = parse("input")

# Generate all the sequences of 2001 prices
sequences = []
changes = []
for buyer in buyers:
    number = buyer
    sequence = [number]
    for _ in range(2000):
        number = find_next(number)
        sequence.append(number % 10)    # Get the least significant digit
    sequences.append(sequence)

    # Generate lists of all 2000 changes
    change = []
    for i in range(len(sequence) - 1):
        change.append(sequence[i+1] - sequence[i])
    changes.append(changes)

print(len(buyers))





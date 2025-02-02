import sys
from math import floor, ceil


def progress_bar(progress, total, length=40):
    percent = progress / total
    bar = "#" * floor(percent * length) + "-" * (length - ceil(percent * length))
    line = "\r[" + bar + "]" + format(percent*100, ".2f") + "%"
    sys.stdout.write(line)
    sys.stdout.flush()


def mix_prune(secret, value):
    secret =  secret ^ value
    return secret % 16777216


def find_next(secret):
    secret = mix_prune(secret, secret << 6)
    secret = mix_prune(secret, secret >> 5)
    secret = mix_prune(secret, secret << 11)
    return secret


def parse(fp):
    with open(fp, "r") as file:
        nums = file.readlines()
    return [int(num) for num in nums]


buyers = [1, 10, 100, 2024]
buyers = parse("input")

# Generate all the sequences of 2001 prices
print("\nGenerating secret numbers")
sequences = []
for i, buyer in enumerate(buyers):
    number = buyer
    sequence = [number]
    for k in range(2000):
        number = find_next(number)
        sequence.append(number % 10)    # Get the least significant digit

        progress_bar(i * 2000 + k, len(buyers) * 2000)
    sequences.append(sequence)

# Generate lists of all 2000 changes
print("\nGenerating difference sequences")
changes = []
for k, sequence in enumerate(sequences):
    change = []
    for i in range(len(sequence) - 1):
        change.append(sequence[i+1] - sequence[i])
        progress_bar(k * (len(sequence) - 1) + i, len(sequences) * (len(sequence) - 1))
    changes.append(change)

# Calculate the prices of every 4 digit subsequence
print("\nFinding maximum sequence prices")
prices = []
for k, change in enumerate(changes):
    price = {}
    prices.append(price)
    for i in range(3, len(change) - 4 + 1):    # range ends 4 digits before the end as the sequence is 4 digits long
        sub = tuple(change[i : i + 4])
        if sub not in price:
            price[sub] = sequences[k][i+4]   # The subsequence of change starting at index i corresponds to the price at index i+4 of the price sequence
        progress_bar(k * (len(change) - 4 + 1 - 3) + i, (len(change) - 4 + 1 - 3) * len(changes))

# Get a set of all the sequences across all buyers
subsequences = set()
for price in prices:
    subsequences.update(set(price.keys()))

# Calculate the sum of the prices for each buyer
print("\nCalculating prices")
highest = (None, float("-inf"))    # (sequence, price)
for i, subsequence in enumerate(subsequences):
    sum = 0
    for k, price in enumerate(prices):
        if subsequence in price:
            sum += price[subsequence]

        progress_bar(i * len(prices) + k, len(prices) * len(subsequences))

    if sum > highest[1]:
        highest = (subsequence, sum)

print()
print(highest)
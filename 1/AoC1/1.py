# Import and parse file
with open("input.txt", "r") as file:
    A = []
    B = []

    lists = [line.split("   ") for line in file.readlines()]
    for ab in lists:
        try:
            A.append(int(ab[0].replace("\n", "")))
            B.append(int(ab[1].replace("\n", "")))
        except:
            pass

A.sort()
B.sort()

pointer = 0
score = 0

for num in A:
    prev = pointer
    try:
        while B[pointer] != num:
            pointer += 1
        while B[pointer] == num:
            score += num
            pointer += 1
    except IndexError:
        pointer = prev

print(score)

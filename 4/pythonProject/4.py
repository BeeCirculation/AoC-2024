with open("input.txt", "r") as file:
    wordsearch = file.readlines()

target = "XMAS"
counter = 0

def check_letter(input, coords, target):
    if input[coords[0]][coords[1]] != target[0]:
        return 0

    output = 0
    for i in range(coords[0] - 1, coords[0] + 2):
        for k in range(coords[1] - 1, coords[1] + 2):
            if i == coords[0] and k == coords[1]:
                continue

            try:
                if input[i][k] != target[1]:
                    continue
            except IndexError:
                continue

            direction = (i - coords[0], k - coords[1])

            def check_dir(input_, coords_, target_, dir_):
                try:
                    if input_[coords_[0]][coords_[1]] == target_:
                        return 1
                except IndexError:
                    return 0
                #for char in target_:
                coords_ = tuple(c + d for c, d in zip(coords_, dir_))
                try:
                    if target_[0] == input[coords_[0]][coords_[1]]:
                        return check_dir(input_, tuple(c + d for c, d in zip(coords_, dir_)), target_[1:], dir_)
                except IndexError:
                    return 0
                return 0

            output += check_dir(input, tuple(c + d for c, d in zip(coords, direction)), target[2:], direction)
    return output



test = ["AMSAMX",
        "AXVKAM",
        "AKMAKM",
        "KXMASM",
        "AKMKSM"]

counter = 0
for i in range(len(wordsearch)):
    for k in range(len(wordsearch[i])):
        if wordsearch[i][k] == "A":
            cross = True
            try:
                corners = [(-1,-1), (-1,1), (1,-1), (1,1)]
                letters = ["M", "S"]
                for corner in corners:
                    if wordsearch[i+corner[0]][k+corner[1]] not in letters:
                        cross = False
                    if wordsearch[i+corner[0]][k+corner[1]] == wordsearch[i+ -1 * corner[0]][k+ -1 * corner[1]]:
                        cross = False
            except IndexError:
                continue
            if cross:
                counter += 1


print(counter)
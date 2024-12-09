def parse(fp):
    with open(fp, "r") as f:
        return f.readline()[:-1]


def decompress(map):
    output = []
    is_file = True
    ID = 0
    for char in map:
        if is_file:
            for _ in range(int(char)):
                output.append(ID)
            ID += 1
        else:
            for _ in range(int(char)):
                output.append(None)
        is_file = not is_file
    return output


def swap(lst, a, b):
    temp = lst[a]
    lst[a] = lst[b]
    lst[b] = temp


def find_last_file_block(disk):
    for i in range(0, len(disk))[::-1]:
        if disk[i] is not None:
            return i
    return None


def reorder(disk):
    file_block = find_last_file_block(disk)
    empty = disk.index(None)

    while empty < file_block:
        swap(disk, file_block, empty)
        file_block = find_last_file_block(disk)
        empty = disk.index(None)


def checksum(disk):
    sum = 0
    for i, block in enumerate(disk):
        if block is None:
            continue
        sum += i * block
    return sum

disk_map = parse("input")
#disk_map = parse("test")

decompressed = decompress(disk_map)
reorder(decompressed)
sum = checksum(decompressed)
print(sum)




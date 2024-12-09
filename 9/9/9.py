from os.path import isfile

from more_itertools.more import first


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


def part1(disk):
    disk_ = disk.copy()
    reorder(disk_)
    sum = checksum(disk_)
    print(sum)


def partition(disk):
    out = [[]]

    ID_last = "none"
    for ID in disk:
        if ID == ID_last or ID_last == "none":
            out[-1].append(ID)
        else:
            out.append([ID])

        ID_last = ID
    return out


def defrag(disk: list):
    disk_ = disk.copy()

    i = len(disk_)
    while i >= 0:
        i -= 1
        last_file = disk_[i]
        if last_file[0] is None:
            continue

        for k in range(i):
            first_empty = disk_[k]
            if first_empty[0] is not None:
                continue
            if len(first_empty) < len(last_file):
                continue

            if len(first_empty) == len(last_file):
                swap(disk_, i, k)
            else:
                diff = len(first_empty) - len(last_file)
                split1 = [None] * len(last_file)
                split2 = [None] * diff
                disk_.pop(k)
                disk_.insert(k, split1)
                disk_.insert(k+1, split2)
                i += 1
                swap(disk_, k, i)
            break
    return disk_


def departition(disk):
    out = []
    for part in disk:
        for block in part:
            out.append(block)
    return out

def part2(disk):
    disk_ = disk.copy()
    parts = partition(disk_)
    defragged = departition(defrag(parts))
    return checksum(defragged)


disk_map = parse("input")
#disk_map = parse("test")

decompressed = decompress(disk_map)

print(part2(decompressed))
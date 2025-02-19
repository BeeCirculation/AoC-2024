from itertools import product


def parse(fp: str) -> tuple[list[list[str]], list[list[str]]]:
    """
    Reads the input file and outputs the locks and keys

    Args:
        fp: The path to the file

    Returns:
        The lists of locks and keys
    """
    with open(fp, "r") as file:
        schematics = file.read().split("\n\n")

    locks = []
    keys = []
    for schematic in schematics:
        # The end of the file may have a hidden newline which must be removed
        while schematic[-1] not in ".#":
            schematic = schematic[:-1]

        # Sort into locks and keys
        lines = schematic.split("\n")
        if lines[0] == "....." and lines[-1] == "#####":
            keys.append(lines)
        elif lines[0] == "#####" and lines[-1] == ".....":
            locks.append(lines)

    return locks, keys


def convert(schematic: list[str]) -> list[int]:
    """
    Converts the schematic of a lock or key into its integer representation

    Args:
        schematic: The schematic of the lock or key

    Returns:
        A list of integers representing the heights at each column
    """
    heights = []
    for i in range(5):
        height = -1
        for row in schematic:
            if row[i] == "#":
                height += 1
        heights.append(height)

    return heights


def convert_all(schematics: list[list[str]]) -> list[list[int]]:
    converted_schematics = []
    for schematic in schematics:
        converted_schematics.append(convert(schematic))
    return converted_schematics


def try_lock(lock: list[int], key: list[int], depth: int = 5) -> bool:
    """
    Determines whether a key and lock combination fit together

    Args:
        lock: The lock to be tested
        key: The key to be tested
        depth: The depth of the lock; the length that the heights should add up to

    Returns:
        True: If they fit together
        False: If they don't fit together
    """
    for l, k in zip(lock, key):
        if l + k > 5:
            return False
    return True


locks, keys = parse("input")
locks = convert_all(locks)
keys = convert_all(keys)

working_pairs = []
for lock, key in product(locks, keys):
    if try_lock(lock, key):
        working_pairs.append((lock, key))
        print(lock, key)

print(len(working_pairs))





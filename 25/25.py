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


locks, keys = parse("test")
locks = convert_all(locks)
keys = convert_all(keys)

print(locks)
print(keys)




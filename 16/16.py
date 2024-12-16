from MyVector import Vector

def parse(fp):
    with open(fp, "r") as file:
        return [list(line) for line in file.read().split("\n")]


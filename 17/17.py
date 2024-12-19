def parse(fp):
    with open(fp, "r") as file:
        registers, program = file.read().split("\n\n")
        registers = registers.split("\n")
        a, b, c = tuple(int(r.split(": ")[1]) for r in registers)

        program = [int(o) for o in program.split(": ")[1].split(",")]
    return a, b, c, program

A, B, C, program = parse("test")

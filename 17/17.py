def parse(fp):
    with open(fp, "r") as file:
        registers, program = file.read().split("\n\n")
        registers = registers.split("\n")
        a, b, c = tuple(int(r.split(": ")[1]) for r in registers)

        program = [int(o) for o in program.split(": ")[1].split(",")]
    return a, b, c, program

A, B, C, program = parse("test")
IC = 0
output = []

operands = {0: 0,
            1: 1,
            2: 2,
            3: 3,
            4: A,
            5: B,
            6: C,
            7: None}

def adv(op):
    global A
    A = A / pow(2, operands[op])
    return 2

def bxl(op):
    global B
    B = B ^ op
    return 2

def bst(op):
    global B
    B = operands[op] % 8
    return 2

def jnz(op):
    global A, IC
    if A == 0:
        return 2

    IC = op
    return 0

def bxc(op):
    global B, C
    B = B ^ C
    return 2

def out(op):
    global output
    output.append(operands[op] % 8)
    return 2

def bdv(op):
    global B, A
    B = A / pow(2, operands[op])
    return 2

def cdv(op):
    global A, C
    A = C / pow(2, operands[op])

opcodes = {0: adv,
           1: bxl,
           2: bst,
           3: jnz,
           4: bxc,
           5: out,
           6: bdv,
           7: cdv}

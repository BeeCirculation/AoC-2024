def parse(fp):
    with open(fp, "r") as file:
        registers, program = file.read().split("\n\n")
        registers = registers.split("\n")
        a, b, c = tuple(int(r.split(": ")[1]) for r in registers)

        program = [int(o) for o in program.split(": ")[1].split(",")]
    return a, b, c, program

A, B, C, program = parse("test2")
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


def write(func):
    def wrapper(*args):
        #print(func.__name__, *args)
        return func(*args)
    return wrapper


@write
def adv(op):
    operands[4] = operands[4] // pow(2, operands[op])
    return 2

@write
def bxl(op):
    operands[5] = operands[5] ^ op
    return 2

@write
def bst(op):
    operands[5] = operands[op] % 8
    return 2

@write
def jnz(op):
    global IC
    if operands[4] == 0:
        return 2

    IC = op
    return 0

@write
def bxc(op):
    operands[5] = operands[5] ^ operands[6]
    return 2

@write
def out(op):
    output.append(operands[op] % 8)
    return 2

@write
def bdv(op):
    operands[5] = operands[4] // pow(2, operands[op])
    return 2

@write
def cdv(op):
    operands[6] = operands[4] // pow(2, operands[op])
    return 2

opcodes = {0: adv,
           1: bxl,
           2: bst,
           3: jnz,
           4: bxc,
           5: out,
           6: bdv,
           7: cdv}


def run_program(prog):
    global IC, output, start
    while IC < len(prog):
        operation = opcodes[prog[IC]]
        operand = prog[IC+1]
        step = operation(operand)
        IC += step
        #print(f"{IC}: A={operands[4]}, B={operands[5]}, C={operands[6]}, out={output}")
        #input()
    IC = 0
    out = output.copy()
    output = []
    return out

start = 0
while run_program(program) != program:
    start += 1
    operands[4] = start
    operands[5] = B
    operands[6] = C
    print(start)
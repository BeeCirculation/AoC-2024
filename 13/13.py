class Vector:
    def __init__(self, data):
        self.data = data
        self.dimension = len(data)

    def __add__(self, other: "Vector"):
        if isinstance(other, int) or isinstance(other, float):
            return Vector([a + other for a in self.data])

        if self.dimension != other.dimension:
            raise ValueError

        return Vector([a + b for a, b in zip(self.data, other.data)])

    def __mul__(self, other):
        if not isinstance(other, int):
            raise ValueError

        return Vector([a * other for a in self.data])

    def __getitem__(self, item):
        return self.data[item]

    def __eq__(self, other):
        if self.dimension != other.dimension:
            return False
        for a,b in zip(self.data, other.data):
            if a != b:
                return False
        return True

    def __str__(self):
        return str(self.data).replace("[", "<").replace("]", ">")

def parse(fp):
    with open(fp, "r") as file:
        line = file.readline()
        output = [{}]
        i = 0
        while line:
            if line == "\n":
                line = file.readline()
                i += 1
                output.append({})
                continue
            label_data = line.split(": ")
            label = label_data[0]
            data = [int(num[2:]) for num in label_data[1].split(", ")]
            output[i].update({label: Vector(data)})
            line = file.readline()

    return output


def handle_machine(machine: dict):
    def find_multiples(A, B, target):
        valid = []
        # check all possible multiples up to 100
        a_test = A[0]
        i = 0
        while a_test < target[0]:
            i += 1
            a_test = i * A[0]
            # For any multiple of A's x coordinate, find if some multiple of B's x coordinate can sum to the target
            remainder = target[0] - a_test
            if remainder % B[0] == 0:
                valid.append((i, remainder // B[0]))

        output = []
        # For all multiples combinations that work for the x coordinate, check if they also work for the y coordinate
        for A_multiples, B_multiples in valid:
            if (A_multiples * A[1]) + (B_multiples * B[1]) == target[1]:
                output.append((A_multiples, B_multiples))
        return output

    def find_multiples2(A, B , target):
        ax, ay = A[0], A[1]
        bx, by = B[0], B[1]
        px, py = target[0], target[1]

        # These equations come from solving the simultaneous equations for i and j:
        #       Ax * i + Bx * j = Px
        #       Ay * i + By * j = Py
        # These equations dont necessarily give integer solutions so we use floor division to give integers
        # and then the solutions must be checked to see if they still satisfy the original equations
        i = ((py * bx) - (by * px)) // ((ay * bx) - (ax * by))
        j = (px - (ax * i)) // bx

        def check(i, j):
            if i < 0 or j < 0:
                return False
            return (A * i) + (B * j) == target

        return [(i, j)] if check(i, j) else []

    multiples = find_multiples2(machine["Button A"], machine["Button B"], machine["Prize"])

    #Find the price of each multiple and sort to find the cheapest
    if len(multiples) != 0:
        price_a, price_b = 3, 1
        prices = {multiple: (price_a * multiple[0]) + (price_b * multiple[1]) for multiple in multiples}
        prices = sorted(prices.items(), key=lambda x: x[1])
        return prices[0][1]
    else:
        return 0


machines = parse("input")

# Adds the extra number for part 2
for machine in machines:
    machine["Prize"] += 10_000_000_000_000

total = 0
for machine in machines:
    total += handle_machine(machine)
print(total)

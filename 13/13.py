class Vector:
    def __init__(self, data):
        self.data = data
        self.dimension = len(data)

    def __add__(self, other: "Vector"):
        if self.dimension != other.dimension:
            raise ValueError

        return Vector([a + b for a, b in zip(self.data, other.data)])

    def __mul__(self, other):
        if not isinstance(other, int):
            raise ValueError

        return Vector([a * other for a in self.data])

    def __getitem__(self, item):
        return self.data[item]

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
        for i in range(1, 101):
            # For any multiple of A's x coordinate, find if some multiple of B's x coordinate can sum to the target
            remainder = target[0] - (A[0] * i)
            if remainder % B[0] == 0:
                valid.append((i, remainder // B[0]))

        output = []
        # For all multiples combinations that work for the x coordinate, check if they also work for the y coordinate
        for A_multiples, B_multiples in valid:
            if (A_multiples * A[1]) + (B_multiples * B[1]) == target[1]:
                output.append((A_multiples, B_multiples))
        return output

    multiples = find_multiples(machine["Button A"], machine["Button B"], machine["Prize"])
    if len(multiples) != 0:
        price_a, price_b = 3, 1
        prices = {multiple: (price_a * multiple[0]) + (price_b * multiple[1]) for multiple in multiples}
        prices = sorted(prices.items(), key=lambda x: x[1])
        return prices[0][1]
    else:
        return 0


machines = parse("input")
total = 0
for machine in machines:
    total += handle_machine(machine)
print(total)

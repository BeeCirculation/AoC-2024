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


machines = parse("test")
print(machines)

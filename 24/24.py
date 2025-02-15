def parse(fp):
    with open(fp, "r") as file:
        starts, gates = file.read().split("\n\n")   # splits the two sections of initial wires values and gates
        starts = [start.split(": ") for start in starts.split("\n")]  # splits starts into its name and value
        starts = {name: int(val) for name, val in starts}

        inputs, outputs = zip(*[gate.split(" -> ") for gate in gates.split("\n")][:-1])
        inputs = [i.split(" ") for i in inputs]
        gate_data = [i + [o] for i, o in zip(inputs, outputs)]
        gates = []
        for i0, gate, i1, o in gate_data:
            gates.append({"i0": i0, "i1": i1, "gate": gate, "o": o})

        return starts, gates


# ALGORITHM
#
# add starting values to known outputs
# all other wires are unknown
# LOOP START
# search unknown wires for decipherable outputs (gates where both inputs are known)
# determine output
# add that output to known outputs, remove from unknown
# if unknown is empty BREAK
# LOOP END

funcs = {"AND": lambda x, y: x and y, "OR": lambda x, y: x or y, "XOR": lambda x, y: x ^ y}



# Initialise sets
known, unknown = parse("input")

while unknown:
    # Find decipherables
    decipherables = [gate for gate in unknown if gate["i0"] in known and gate["i1"] in known]

    for decipherable in decipherables:
        i0, gate, i1, o = decipherable["i0"], decipherable["gate"], decipherable["i1"], decipherable["o"]
        # Calculate results
        result = funcs[gate](known[i0], known[i1])

        # Update sets
        known.update({o: result})
        unknown.remove(decipherable)


# Extract only the output wires
outputs = {k: v for k, v in known.items() if k.startswith("z")}
# Ensure they are in the correct order and convert to decimal
num = "".join([str(o[1]) for o in sorted(outputs.items(), key=lambda x: x[0], reverse=True)])
print(num)
num = int(num, 2)
print(num)



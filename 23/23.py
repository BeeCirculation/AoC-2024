from itertools import permutations, combinations


def parse(fp):
    with open(fp, "r") as file:
        return [tuple(line.replace("\n", "").split("-")) for line in file.readlines()]


def generate_adj_matrix(edges: list[tuple], verts: list) -> dict[any, dict[any, int]]:
    """
    Creates the adjacency matrix of a graph represented by a vertex and edge set

    Args:
        edges: The set of edges as a tuple of vertices
        verts: The set of vertices

    Returns:
        A dictionary where the keys are the vertices and the values are a dictionary where the keys are the vertices
         and the values are the adjacency value; 1 if the vertices are adjacent and 0 if they are not
    """
    vertices = verts.copy()

    # Initialise matrix
    matrix = {}
    pairs = list(permutations(vertices, 2))
    for a, b in pairs:
        if a in matrix:
            matrix[a].update({b: 0})
        else:
            matrix[a] = {b: 0}

    # Add adjacent cells
    for a, b in edges:
        matrix[a][b] = 1
        matrix[b][a] = 1

    return matrix


connections = parse("input")
#connections = parse("test")

vertices = set([c[0] for c in connections] + [c[1] for c in connections])

# For all possible subsets, check if all elements are adjacent to eachother
subsets = combinations(vertices, 3)
adj_matrix = generate_adj_matrix(connections, vertices)

cliques = []
for subset in subsets:
    pairs = combinations(subset, 2)
    clique = True
    for a, b in pairs:
        if adj_matrix[a][b] != 1:
            clique = False
    if clique:
        cliques.append(subset)

valid_cliques = []
for clique in cliques:
    contains_t = False
    for computer in clique:
        if computer[0] == "t":
            contains_t = True
            break
    if contains_t:
        valid_cliques.append(clique)

print(len(valid_cliques))
for valid_clique in valid_cliques:
    print(valid_clique)
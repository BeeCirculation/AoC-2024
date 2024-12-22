from MyGraph import dijkstra, get_branches
from MyVector import Grid, Vector, UP, DOWN, LEFT, RIGHT

def parse(fp):
    with open(fp, "r") as file:
        lines = [line[:-1] for line in file.readlines() if line != "\n"]

    g = Grid(len(lines[0]), len(lines), ".")
    for i, line in enumerate(lines):
        g.set_row(g.height - 1 - i, list(line))

    return g


def adj(current, distances):
    distances = [d.change_dimension(2) for d in [UP, DOWN, LEFT, RIGHT]]
    for d in distances:
        if track_base[current + d] != "#":
            yield current + d, 1


track_base = parse("test")
print(track_base)
s = track_base.find("S")[0]
e = track_base.find("E")[0]


def vis(current, distances, visited, q):
    track_vis = track_base.__deepcopy__()

    for _, a in q:
        track_vis[a] = "⚬"

    for a in visited:
        track_vis[a] = "○"

    def get_children(node):
        return [distances[node][1]] if distances[node][1] else None

    path_to_current = get_branches(current, get_children)
    for a in path_to_current[0]:
        track_vis[a] = "●"

    track_vis[current] = "❖"

    print(f"\033[{track_vis.height + 1}A" + str(track_vis))
    input("\033[1A")


length, path = dijkstra(s, adj, e, visualiser=vis)
CHEAT_LEN = 2


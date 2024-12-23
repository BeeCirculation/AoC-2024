from MyGraph import dijkstra, get_branches
from MyVector import Grid, Vector, UP, DOWN, LEFT, RIGHT

DIRECTIONS = [d.change_dimension(2) for d in [UP, DOWN, LEFT, RIGHT]]

def parse(fp):
    with open(fp, "r") as file:
        lines = [line[:-1] for line in file.readlines() if line != "\n"]

    g = Grid(len(lines[0]), len(lines), ".")
    for i, line in enumerate(lines):
        g.set_row(g.height - 1 - i, list(line))

    return g


def adj(current, distances):
    for d in DIRECTIONS:
        if track_base.in_grid(current + d) and track_base[current + d] != "#":
            yield current + d, 1

def adj2(current, distances):
    for d in DIRECTIONS:
        if track_base.in_grid(current + d):
            yield current + d, 1


track_base = parse("input")
print(track_base)
s = track_base.find("S")[0]
e = track_base.find("E")[0]


def vis(current, distances, visited, q):
    track_vis = track_base.__deepcopy__()

    for _, a in q:
        track_vis[a] = "⚬"

    for a in visited:
        track_vis[a] = "●"

    track_vis[current] = "❖"

    print(f"\033[{track_vis.height + 1}A" + str(track_vis))
    #input("\033[1A")

length, path = dijkstra(s, adj, e, visualiser=vis)

CHEAT_LEN = 20
LIMIT = 100

cheats = {}
saves = {}
path = {spot: i for i, spot in enumerate(path)}
for spot, dist in path.items():
    start_spot = spot.__deepcopy__()

    # Find the diamond of all possible end positions
    end_positions = {}
    for x in range(CHEAT_LEN + 1):
        for y in range(CHEAT_LEN + 1 - x):
            end_positions.update({Vector(x, y) + start_spot: x + y})
            end_positions.update({Vector(x, -y) + start_spot: x + y})
            end_positions.update({Vector(-x, y) + start_spot: x + y})
            end_positions.update({Vector(-x, -y) + start_spot: x + y})
            print(dist/len(path), (x*CHEAT_LEN + y) / 400, end="\r")

    for next_spot, cheat_dist in end_positions.items():
        if not track_base.in_grid(next_spot):
            continue

        if track_base[next_spot] == "#":
            continue
        def vis2(current, distances, visited, q):
            track_vis = track_base.__deepcopy__()

            for _, a in q:
                track_vis[a] = "⚬"

            for a in visited:
                track_vis[a] = "●"

            track_vis[current] = "❖"

            track_vis[spot] = "s"
            track_vis[next_spot] = "e"

            print(f"\033[{track_vis.height + 1}A" + str(track_vis))
            #input("\033[1A")

        if next_spot in path:
            remaining_dist = length - path[next_spot]
        else:
            remaining_dist, _ = dijkstra(next_spot, adj, e, visualiser=None)
        #input("\033[1A")
        if remaining_dist is not None:
            saved = length - (dist + cheat_dist + remaining_dist)
            if saved >= LIMIT:
                cheats.update({(spot, next_spot): saved})
        #input("\033[1A")

for cheat, save in cheats.items():
    if save in saves:
        saves[save] += 1
    else:
        saves[save] = 1
print()
print(saves)
print(sum(saves.values()))

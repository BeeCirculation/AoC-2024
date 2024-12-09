class Graph:
    def __init__(self, vertices=None, edges=None):
        try:
            self.edges = set(edges)
        except TypeError:
            self.edges = set()

        try:
            self.vertices = set(vertices)
        except TypeError:
            self.vertices = set()
            for a,b in self.edges:
                self.add_vertex(a)
                self.add_vertex(b)

    @property
    def order(self):
        return len(self.vertices)

    @property
    def size(self):
        return len(self.edges)

    def add_vertex(self, vertex):
        self.vertices.update({vertex})

    def add_edge(self, edge):
        if edge[0] not in self.vertices or edge[1] not in self.vertices:
            raise ValueError("Edge contains vertices not contained in the graph")
        self.edges.update({edge})

    def add_edge_vertex(self, edge):
        self.add_vertex(edge[0])
        self.add_vertex(edge[1])
        self.add_edge(edge)

    def remove_vertex(self, vertex):
        try:
            self.vertices.remove(vertex)
            self.edges = [edge for edge in self.edges if vertex not in edge]
        except KeyError:
            pass

    def remove_edge(self, edge):
        try:
            self.edges.remove(edge)
        except KeyError:
            pass

    def get_adjacent_to(self, vertex):
        '''Gets all the vertices the given vertex is adjacent to'''
        return [edge[0] for edge in self.edges if vertex == edge[1]]

    def get_adjacent_vertices(self, vertex):
        '''Gets all the vertices that are adjacent to the given vertex'''
        return [edge[1] for edge in self.edges if vertex == edge[0]]

    def degree(self, vertex):
        return len(self.get_adjacent_to(vertex)) + len(self.get_adjacent_vertices(vertex))

    def in_degree(self, vertex):
        return len(self.get_adjacent_to(vertex))

    def out_degree(self, vertex):
        return len(self.get_adjacent_vertices(vertex))

    @property
    def min_degree(self):
        if len(self.vertices) < 1:
            raise ValueError("Graph has no vertices")
        min_in = {"degree": float("inf"), "vertex": None}
        min_out = {"degree": float("inf"), "vertex": None}
        min = {"degree": float("inf"), "vertex": None}
        for vertex in self.vertices:
            in_degree = len(self.get_adjacent_to(vertex))
            out_degree = len(self.get_adjacent_vertices(vertex))
            degree = in_degree + out_degree

            if in_degree < min_in["degree"]:
                min_in = {"degree": in_degree, "vertex": vertex}
            if out_degree < min_out["degree"]:
                min_out = {"degree": out_degree, "vertex": vertex}
            if degree < min["degree"]:
                min = {"degree": degree, "vertex": vertex}
        return {"degree": min, "in": min_in, "out": min_out}

    @property
    def max_degree(self):
        if len(self.vertices) < 1:
            raise ValueError("Graph has no vertices")
        max_in = {"degree": 0, "vertex": None}
        max_out = {"degree": 0, "vertex": None}
        max = {"degree": 0, "vertex": None}
        for vertex in self.vertices:
            in_degree = len(self.get_adjacent_to(vertex))
            out_degree = len(self.get_adjacent_vertices(vertex))
            degree = in_degree + out_degree

            if in_degree > max_in["degree"]:
                max_in = {"degree": in_degree, "vertex": vertex}
            if out_degree > max_out["degree"]:
                max_out = {"degree": out_degree, "vertex": vertex}
            if degree > max["degree"]:
                max = {"degree": degree, "vertex": vertex}
        return {"degree": max, "in": max_in, "out": max_out}

    def shortest_path(self, source, target):
        if source not in self.vertices or target not in self.vertices:
            raise ValueError("Both source and target must be vertices in the graph")

        distances = {vertex: float('inf') for vertex in self.vertices}
        distances[source] = 0
        unvisited = sorted(self.vertices, key=lambda x: distances[x])

        while len(unvisited) > 0:
            current = unvisited[0]
            adjs = self.get_adjacent_vertices(current)
            for adj in adjs:
                dist = distances[current] + 1
                if dist < distances[adj]:
                    distances[adj] = dist
            unvisited.remove(current)
            unvisited = sorted(unvisited, key=lambda x: distances[x])
            if target not in unvisited:
                break

        return distances[target]

    def bfs(self, source):
        output = {source: 0}
        queue = [(source, 0)]
        while len(queue) > 0:
            current = queue[0]
            for vertex in self.get_adjacent_vertices(current[0]):
                if vertex not in queue:
                    queue.append((vertex, current[1] + 1))
                    output.update({vertex: current[1] + 1})
            queue.pop(0)
        return output

    def connected(self, source, target):
        try:
            if self.shortest_path(source, target) != float("inf"):
                return True
            else:
                return False
        except ValueError:
            return False

    def compose(self, relation):
        g = Graph()
        for source, middle_a in self.edges:
            for target in relation.get_adjacent_vertices(middle_a):
                g.add_edge_vertex((source, target))

        return g

    def __str__(self):
        return "Vertices:\n" + str(self.vertices) + "\n\nEdges:\n" + str(self.edges)

    def copy(self):
        return Graph(self.vertices.copy(), self.edges.copy())

def parse_input(file):
    with open(file, "r") as file:
        rules = []
        pages = []

        line = file.readline()
        while line != "\n":
            pair = tuple(int(a) for a in line.split("|"))
            rules.append(pair)
            line = file.readline()


        line = file.readline()
        while line:
            pages.append([int(a) for a in line.split(",")])
            line = file.readline()

    return rules, pages


def check_order(ordering, sequence):
    i = 0
    for item in sequence:
        try:
            while ordering[i] != item:
                i += 1
        except IndexError:
            return False
    return True


pairs, pages = parse_input("input.txt")
#pairs, pages = parse_input("test.txt")

sum = 0
for page in pages:
    relevant_pairs = [(a,b) for a,b in pairs if a in page and b in page]
    ordering = Graph(edges=relevant_pairs)
    order = sorted(ordering.vertices, key= lambda x: ordering.in_degree(x))
    if not check_order(order, page):
        fixed = [x for x in order if x in page]
        median = fixed[len(fixed) // 2]
        sum += median
print(sum)
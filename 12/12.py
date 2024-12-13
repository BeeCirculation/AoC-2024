def parse(fp):
    with open(fp, "r") as file:
        return [line_[:-1] for line_ in file.readlines()]

garden = parse("input")
#garden = parse("test")

class Region:
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def __init__(self, area):
        """
        Initialises the Region
        Args:
            area (list[str]): The area that the region belongs to
        """
        self.grid = area
        self.plots = set()
        self.types = set()
        self.edges = set()

    def __isvalid(self, coord):
        return 0 <= coord[0] < len(self.grid) and 0 <= coord[1] < len(self.grid[0])

    def fill(self, coord):
        """
        Will fill out the region by adding any adjacent plots of the same type from a given co-ordinate

        Args:
            coord (tuple[int, int]): The co-ordinate to start the fill at

        Returns:

        """
        self.plots.add(coord)
        self.types.add(self.grid[coord[0]][coord[1]])

        # Adds adjacent plots to a queue and self.plots
        # Then evaluates the next plot in the queue until there are no more plots
        q = [coord]
        while len(q) > 0:
            current = q[0]
            for direction in Region.directions:
                adj = current[0] + direction[0], current[1] + direction[1]
                if self.__isvalid(adj) and self.grid[adj[0]][adj[1]] in self.types:
                    if adj not in self.plots:
                        q.append(adj)
                        self.plots.add(adj)
            q.pop(0)

    def _find_perimeter(self):
        # For each plot, calculate the number of edges that dont boarder another plot in the region
        # Store the edges (as a pair of plots)
        count = 0
        for plot in self.plots:
            for direction in Region.directions:
                adj = plot[0] + direction[0], plot[1] + direction[1]
                if adj not in self.plots:
                    self.edges.add((plot, adj))
        return self.edges

    def perimeter(self):
        self._find_perimeter()
        return len(self.edges)

    def area(self):
        return len(self.plots)

    def _find_sides(self):
        """
        Finds all the sides of the region. Self._find_perimeter() must be called first to ensure the edges are up to date
        Returns (list[set[tuple[int, int]]]): A list of sides which are represented as sets of edges which are pairs
        of plots which are tuples of a pair of integers

        """
        sides_list = []
        seen_edges = set()
        for edge in self.edges:
            if edge not in seen_edges:
                side = self._find_side(edge)
                seen_edges.update(side)
                sides_list.append(side)
        return sides_list

    def sides(self):
        return len(self._find_sides())

    def _find_side(self, edge: tuple[tuple[int,int], tuple[int,int]]):
        plot, outside = edge
        plot_y, plot_x = plot
        outside_y, outside_x = outside

        # A side is formed by adjacent edges. Edges are adjacent if they are next to eachother and in the same direction
        # So we must find the direction of the edge and check its neighbours

        # The direction vector of plot to outside determines the edge direction
        edge_direction_y, edge_direction_x = outside_y - plot_y, outside_x - plot_x

        # The edge is perpendicular to the direction vector between the plots that define it
        if abs(edge_direction_y) == 1:
            directions = [(0, 1), (0,-1)]
        else:
            directions = [(1,0), (-1,0)]

        # Now based on these directions we must flood fill the edges to find the side
        side = {edge}
        q = [edge]
        while len(q) > 0:
            current = q[0]
            plot, outside = current
            plot_y, plot_x = plot
            outside_y, outside_x = outside
            for direction in directions:
                adj_plot = plot_y + direction[0], plot_x + direction[1]
                adj_outside = outside_y + direction[0], outside_x + direction[1]
                adj = adj_plot, adj_outside

                if adj in self.edges:
                    if adj not in side:
                        side.add(adj)
                        q.append(adj)
            q.pop(0)
        return side


seen_plots = set()
price = 0
for i,line in enumerate(garden):
    for k, char in enumerate(line):
        if (i, k) in seen_plots:
            continue
        r = Region(garden)
        r.fill((i,k))
        perimeter = r.perimeter()
        sides = r.sides()
        price += r.sides() * r.area()

        seen_plots.update(r.plots)
print(price)
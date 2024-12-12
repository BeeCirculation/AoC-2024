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

    def perimeter(self):
        # For each plot, calculate the number of edges that dont boarder another plot in the region
        count = 0
        for plot in self.plots:
            for direction in Region.directions:
                adj = plot[0] + direction[0], plot[1] + direction[1]
                if adj not in self.plots:
                    count += 1
        return count

    def area(self):
        return len(self.plots)


seen_plots = set()
price = 0
for i,line in enumerate(garden):
    for k, char in enumerate(line):
        if (i, k) in seen_plots:
            continue
        r = Region(garden)
        r.fill((i,k))
        price += r.perimeter() * r.area()

        seen_plots.update(r.plots)
print(price)
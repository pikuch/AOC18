# AOC18 day 22


class CaveMap:
    def __init__(self, depth, target_x, target_y):
        self.depth = depth
        self.target_x = target_x
        self.target_y = target_y
        self.max_x = target_x + 5
        self.max_y = target_y + 5
        self.erosion = {}

    def get_erosion_at(self, x, y):
        if (x, y) in self.erosion:
            return self.erosion[(x, y)]
        if x == 0 and y == 0:
            geologic_index = 0
        elif x == self.target_x and y == self.target_y:
            geologic_index = 0
        elif y == 0:
            geologic_index = x * 16807
        elif x == 0:
            geologic_index = y * 48271
        else:
            geologic_index = self.get_erosion_at(x-1, y) * self.get_erosion_at(x, y-1)
        self.erosion[(x, y)] = (geologic_index + self.depth) % 20183
        return self.erosion[(x, y)]

    def generate(self):
        for x in range(self.max_x):
            for y in range(self.max_y):
                self.get_erosion_at(x, y)

    def show(self):
        for y in range(self.max_y):
            for x in range(self.max_x):
                if x == self.target_x and y == self.target_y:
                    print("T", end="")
                elif (x, y) in self.erosion:
                    region = self.erosion[(x, y)] % 3
                    if region == 0:
                        print(".", end="")
                    elif region == 1:
                        print("=", end="")
                    elif region == 2:
                        print("|", end="")
                else:
                    print("?", end="")
            print("")

    def get_risk_level(self):
        risk = 0
        for y in range(self.target_y+1):
            for x in range(self.target_x+1):
                risk += self.erosion[(x, y)] % 3
        return risk


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def parse_data(data):
    lines = data.split("\n")
    depth = int(lines[0].split()[1])
    coords = lines[1].split()
    target_x, target_y = tuple(map(int, coords[1].split(",")))
    return depth, target_x, target_y


def run():
    data = load_data("Day22.txt")
    depth, target_x, target_y = parse_data(data)
    cave_map = CaveMap(depth, target_x, target_y)
    cave_map.generate()
    # cave_map.show()
    print(f"The risk level of the area from the entrance to the target is {cave_map.get_risk_level()}")

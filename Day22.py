# AOC18 day 22
from collections import deque


class CaveMap:
    def __init__(self, depth, target_x, target_y):
        self.depth = depth
        self.target_x = target_x
        self.target_y = target_y
        self.max_x = target_x + 5
        self.max_y = target_y + 5
        self.erosion = {}
        self.types = {}
        self.distance = {}

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
        self.types[(x, y)] = self.erosion[(x, y)] % 3
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
                    region = self.types[(x, y)]
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
                risk += self.types[(x, y)]
        return risk

    def get_time_to_target(self):
        possible_tools = {0: (1, 2), 1: (0, 2), 2: (0, 1)}
        possible_tool2 = {(0, 1): 2, (1, 0): 2, (0, 2): 1, (2, 0): 1, (1, 2): 0, (2, 1): 0}
        dx = {"N": 0, "S": 0, "E": 1, "W": -1}
        dy = {"N": -1, "S": 1, "E": 0, "W": 0}
        self.distance[(0, 0)] = [9**9, 9**9, 9**9]
        to_check = deque()
        to_check.append((0, 0, 1, 0))  # x, y, tool, minutes
        min_minutes = 9**9
        while len(to_check):
            x, y, tool, minutes = to_check.popleft()
            if minutes > min_minutes:  # longer than already found
                continue
            if (x, y) in self.distance:  # already visited
                faster_paths = 0
                for t in possible_tools[self.types[(x, y)]]:
                    dist = minutes if t == tool else minutes + 7
                    if dist < self.distance[(x, y)][t]:
                        self.distance[(x, y)][t] = dist
                        faster_paths += 1
                if faster_paths == 0:
                    continue
            else:
                self.distance[(x, y)] = [-1, -1, -1]
                for t in possible_tools[self.types[(x, y)]]:
                    self.distance[(x, y)][t] = minutes if t == tool else minutes + 7
            if x == self.target_x and y == self.target_y:
                if tool == 1 and minutes < min_minutes:
                    min_minutes = minutes
                elif minutes + 7 < min_minutes:
                    min_minutes = minutes + 7
            # go in 4 directions
            for direction in "NWSE":
                new_x = x + dx[direction]
                new_y = y + dy[direction]
                if new_x < 0 or new_y < 0:
                    continue
                if (new_x, new_y) not in self.types:
                    self.get_erosion_at(new_x, new_y)
                new_type = self.types[(new_x, new_y)]
                if tool != new_type:  # can go without switching
                    to_check.append((new_x, new_y, tool, minutes + 1))
                else:
                    to_check.append((new_x, new_y, possible_tool2[(self.types[(x, y)], new_type)], minutes + 8))
        return min_minutes


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
    data = load_data("Day22test.txt")
    depth, target_x, target_y = parse_data(data)
    cave_map = CaveMap(depth, target_x, target_y)
    cave_map.generate()
    # cave_map.show()
    print(f"The risk level of the area from the entrance to the target is {cave_map.get_risk_level()}")
    print(f"It will take {cave_map.get_time_to_target()} minutes to reach the target")

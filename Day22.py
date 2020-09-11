# AOC18 day 22
from collections import deque
import numpy as np


class CaveMap:
    def __init__(self, depth, target_x, target_y):
        self.depth = depth
        self.target_x = target_x
        self.target_y = target_y
        self.max_x = 100+round(1.5 * max(target_x, target_y))
        self.max_y = 100+round(1.5 * max(target_x, target_y))
        self.erosion = np.zeros((self.max_x, self.max_y), dtype=np.uint32)
        self.type = np.zeros((self.max_x, self.max_y), dtype=np.uint8)
        self.dist = np.full((self.max_x, self.max_y, 3), 9**9, dtype=np.uint32)

    def get_erosion_at(self, x, y):
        if x == 0 and y == 0:
            geologic_index = 0
        elif x == self.target_x and y == self.target_y:
            geologic_index = 0
        elif y == 0:
            geologic_index = x * 16807
        elif x == 0:
            geologic_index = y * 48271
        else:
            geologic_index = self.erosion[x - 1, y] * self.erosion[x, y - 1]
        self.erosion[x, y] = (geologic_index + self.depth) % 20183
        self.type[x, y] = self.erosion[x, y] % 3

    def generate(self):
        for x in range(self.max_x):
            for y in range(self.max_y):
                self.get_erosion_at(x, y)

    def show(self):
        for y in range(self.max_y):
            for x in range(self.max_x):
                if x == self.target_x and y == self.target_y:
                    print("T", end="")
                else:
                    region = self.type[x, y]
                    if region == 0:
                        print(".", end="")
                    elif region == 1:
                        print("=", end="")
                    elif region == 2:
                        print("|", end="")
            print("")

    def get_risk_level(self):
        risk = 0
        for y in range(self.target_y + 1):
            for x in range(self.target_x + 1):
                risk += self.type[x, y]
        assert risk == np.sum(self.type[:self.target_x + 1, :self.target_y + 1])
        return risk

    def get_time_to_target(self):
        dx = {"N": 0, "S": 0, "E": 1, "W": -1}
        dy = {"N": -1, "S": 1, "E": 0, "W": 0}
        self.dist[0, 0, 1] = 0
        to_check = deque()
        to_check.append((0, 0, 1, 0))  # x, y, tool, minutes
        while len(to_check):
            x, y, tool, minutes = to_check.popleft()
            if self.dist[x, y, tool] < minutes:
                continue
            print(f"\rdistance: {x + y}, paths to check: {len(to_check)}", end="")
            if x == self.target_x and y == self.target_y and tool == 1:
                continue
            if minutes >= self.dist[self.target_x, self.target_y, 1]:
                continue
            # go in 4 directions
            for direction in "NWSE":
                new_x = x + dx[direction]
                new_y = y + dy[direction]
                if new_x < 0 or new_y < 0:
                    continue
                if tool != self.type[new_x, new_y] and minutes + 1 < self.dist[new_x, new_y, tool]:
                    self.dist[new_x, new_y, tool] = minutes + 1
                    to_check.append((new_x, new_y, tool, minutes + 1))
            # change equipment
            new_tool = (~ (tool | self.type[x, y])) & 3
            if minutes + 7 < self.dist[x, y, new_tool]:
                self.dist[x, y, new_tool] = minutes + 7
                to_check.append((x, y, new_tool, minutes + 7))

        print(" done!")
        return self.dist[self.target_x, self.target_y, 1]


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
    print("Preparing the grid...")
    cave_map.generate()
    # cave_map.show()
    print(f"The risk level of the area from the entrance to the target is {cave_map.get_risk_level()}")
    print(f"It will take {cave_map.get_time_to_target()} minutes to reach the target")

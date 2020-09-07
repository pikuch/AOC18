# AOC18 day 18
import numpy as np


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def parse_data(data):
    area = np.zeros((len(data), len(data[0])), dtype=np.uint8)
    for row in range(area.shape[0]):
        for col in range(area.shape[1]):
            if data[row][col] == "|":
                area[row, col] = 1
            elif data[row][col] == "#":
                area[row, col] = 2
            else:
                pass  # there is already a zero in place
    return area


def draw(area):
    for row in range(area.shape[0]):
        for col in range(area.shape[1]):
            if area[row, col] == 0:
                print("·", end="")
            elif area[row, col] == 1:
                print("|", end="")
            else:
                print("#", end="")
        print("")


def apply_rule(row, col, area):
    counts = {1: 0, 2: 0}
    row_low = 0 if row == 0 else -1
    col_low = 0 if col == 0 else -1
    row_high = 1 if row == area.shape[0] - 1 else 2
    col_high = 1 if col == area.shape[1] - 1 else 2
    for dr in range(row_low, row_high):
        for dc in range(col_low, col_high):
            if dr == 0 and dc == 0:
                continue
            if area[row + dr, col + dc]:
                counts[area[row + dr, col + dc]] += 1
    if area[row, col] == 0:
        if counts[1] >= 3:
            return 1
        else:
            return 0
    if area[row, col] == 1:
        if counts[2] >= 3:
            return 2
        else:
            return 1
    if area[row, col] == 2:
        if counts[1] >= 1 and counts[2] >= 1:
            return 2
        else:
            return 0


def step(area):
    new_area = np.empty_like(area)
    for row in range(area.shape[0]):
        for col in range(area.shape[1]):
            new_area[row, col] = apply_rule(row, col, area)
    return new_area


def resources_after_minutes(area, n):
    seen = {}
    i = 0
    while i < n:
        i += 1
        area = step(area)
        print(f"\rcalculating step {i} ", end="")
        h = hash(area.tostring())
        if h in seen:
            period = i - seen[h]
            i += period * ((n - i) // period)
        else:
            seen[h] = i

    return np.sum(area == 1) * np.sum(area == 2)


def run():
    data = load_data("Day18.txt").split("\n")
    area = parse_data(data)
    res10 = resources_after_minutes(area, 10)
    print(f"Resource value after 10 minutes is {res10}")
    res1e9 = resources_after_minutes(area, 10**9)
    print(f"Resource value after 1000000000 minutes is {res1e9}")

# AOC18 day 13


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def interpret(data):
    carts = []
    tracks = []
    for row in range(len(data)):
        current = list(data[row])
        for col in range(len(current)):
            if current[col] == "<":
                carts.append([col, row, "W", 0])
                current[col] = "-"
            elif current[col] == ">":
                carts.append([col, row, "E", 0])
                current[col] = "-"
            elif current[col] == "^":
                carts.append([col, row, "N", 0])
                current[col] = "|"
            elif current[col] == "v":
                carts.append([col, row, "S", 0])
                current[col] = "|"
        tracks.append(current)
    return carts, tracks


def move_cart(i, carts, tracks):
    x_change = {"N": 0, "S": 0, "E": 1, "W": -1}
    y_change = {"N": -1, "S": 1, "E": 0, "W": 0}
    dir_change = {("N", "\\"): "W", ("N", "/"): "E",
                  ("S", "\\"): "E", ("S", "/"): "W",
                  ("E", "\\"): "S", ("E", "/"): "N",
                  ("W", "\\"): "N", ("W", "/"): "S"}
    cross_change = {("N", 0): "W", ("N", 1): "N", ("N", 2): "E",
                    ("S", 0): "E", ("S", 1): "S", ("S", 2): "W",
                    ("E", 0): "N", ("E", 1): "E", ("E", 2): "S",
                    ("W", 0): "S", ("W", 1): "W", ("W", 2): "N"}
    # move
    carts[i][0] += x_change[carts[i][2]]
    carts[i][1] += y_change[carts[i][2]]
    # turn
    track = tracks[carts[i][1]][carts[i][0]]
    if track in "/\\":
        carts[i][2] = dir_change[(carts[i][2], track)]
    elif track == "+":
        carts[i][2] = cross_change[(carts[i][2], carts[i][3])]
        carts[i][3] = (carts[i][3] + 1) % 3


def collided(i, carts):
    for j in range(len(carts)):
        if i != j:
            if carts[i][0] == carts[j][0] and carts[i][1] == carts[j][1]:
                return True
    return False


def remove_collided(i, carts):
    for j in range(len(carts)):
        if i != j:
            if carts[i][0] == carts[j][0] and carts[i][1] == carts[j][1]:
                carts[i][1] = -10
                carts[j][1] = -10


def simulate(carts, tracks):
    while True:
        carts.sort(key=lambda c: (c[1], c[0]))
        for i in range(len(carts)):
            move_cart(i, carts, tracks)
            if collided(i, carts):
                return carts[i][0], carts[i][1]


def simulate_last(carts, tracks):
    carts.sort(key=lambda c: (c[1], c[0]))
    while True:
        for i in range(len(carts)):
            move_cart(i, carts, tracks)
            remove_collided(i, carts)
        carts.sort(key=lambda c: (c[1], c[0]))
        if carts[0][1] < 0:
            carts = carts[2:]
        if len(carts) < 2:
            return carts[0][0], carts[0][1]


def run():
    data = load_data("Day13.txt").split("\n")
    carts, tracks = interpret(data)
    print(f"The first crash happens at {simulate(carts, tracks)}")
    carts, tracks = interpret(data)
    print(f"The last cart is at {simulate_last(carts, tracks)}")

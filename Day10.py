# AOC18 day 10


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def parse_data(data):
    stars = []
    for line in data:
        words = line.translate(str.maketrans("=<>,", "    ")).split()
        stars.append({"x": int(words[1]), "y": int(words[2]), "vx": int(words[4]), "vy": int(words[5])})
    return stars


def print_message(stars):
    prev_min_x, prev_max_x = -9**9, 9**9
    steps = 0
    while True:
        steps += 1
        min_x, max_x = 9**9, -9**9
        for star in stars:
            star["x"] += star["vx"]
            star["y"] += star["vy"]
            if star["x"] < min_x:
                min_x = star["x"]
            if star["x"] > max_x:
                max_x = star["x"]
        if prev_max_x - prev_min_x < max_x - min_x:  # the tipping point
            steps -= 1
            break
        prev_min_x = min_x
        prev_max_x = max_x

    coords = set()
    min_y, max_y = 9 ** 9, -9 ** 9
    for star in stars:
        star["x"] -= star["vx"]
        star["y"] -= star["vy"]
        if star["y"] < min_y:
            min_y = star["y"]
        if star["y"] > max_y:
            max_y = star["y"]
        coords.add((star["x"], star["y"]))

    for y in range(max_y - min_y + 1):
        for x in range(prev_max_x - prev_min_x + 1):
            if (x + prev_min_x, y + min_y) in coords:
                print("*", end="")
            else:
                print(" ", end="")
        print("")
    return steps


def run():
    data = load_data("Day10.txt")
    stars = parse_data(data.split("\n"))
    print(f"The message is:")
    steps = print_message(stars)  # AHFGRKEE
    print(f"You would have to wait {steps} seconds")

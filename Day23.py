# AOC18 day 23
from collections import namedtuple
from itertools import product


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def get_nanobots(data):
    nanobots = []
    Bot = namedtuple("Bot", ["x", "y", "z", "r"])
    for line in data.split("\n"):
        words = line.translate(str.maketrans("<>=,", "    ")).split()
        bot = Bot(int(words[1]), int(words[2]), int(words[3]), int(words[5]))
        nanobots.append(bot)
    return nanobots


def distance(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1]) + abs(a[2]-b[2])


def count_in_range_of_bot(strongest, nanobots):
    in_range = 0
    for bot in nanobots:
        if strongest.r >= distance(strongest, bot):
            in_range += 1
    return in_range


def find_strongest(nanobots):
    strongest = nanobots[0]
    for bot in nanobots:
        if bot.r > strongest.r:
            strongest = bot
    return strongest


def get_maxima(nanobots):
    maxima = [9**9] * 3
    for bot in nanobots:
        if abs(bot.x) > maxima[0]:
            maxima[0] = bot.x
        if abs(bot.y) > maxima[1]:
            maxima[1] = bot.y
        if abs(bot.z) > maxima[2]:
            maxima[2] = bot.z
    return maxima


def count_in_range_of_point(x, y, z, nanobots):
    in_range = 0
    for bot in nanobots:
        if bot.r >= distance((x, y, z), bot):
            in_range += 1
    return in_range


def remove_values(val, counts):
    to_remove = []
    for item in counts:
        if item[3] == val:
            to_remove.append(item)
    for item in to_remove:
        counts.remove(item)


def find_center(counts):
    xx, yy, zz = 0, 0, 0
    n = 0
    for point in counts:
        xx += point[0] * point[3]
        yy += point[1] * point[3]
        zz += point[2] * point[3]
        n += point[3]
    xx //= n
    yy //= n
    zz //= n
    return xx, yy, zz


def remove_below_max(counts):
    max_bots = 0
    for point in counts:
        if point[3] > max_bots:
            max_bots = point[3]
    to_remove = []
    for item in counts:
        if item[3] < max_bots:
            to_remove.append(item)
    for item in to_remove:
        counts.remove(item)


def find_best_spot_distance(nanobots):
    base_x, base_y, base_z = 0, 0, 0
    range_x, range_y, range_z = 9**9, 9**9, 9**9
    last_max = [0, 0, 0, 0]
    while range_x + range_y + range_z > 1:
        counts = []
        for x, y, z in product(range(-5, 5), range(-5, 5), range(-5, 5)):
            bots_in_range = count_in_range_of_point(base_x + x * range_x//10,
                                                    base_y + y * range_y//10,
                                                    base_z + z * range_z//10,
                                                    nanobots)
            counts.append((base_x + x * range_x//10,
                           base_y + y * range_y//10,
                           base_z + z * range_z//10,
                           bots_in_range))
        remove_below_max(counts)
        if counts[0][3] < last_max[3]:
            counts = [last_max]

        if len(counts):
            base_x, base_y, base_z = find_center(counts)

        range_x = round(range_x * 0.9 - 1)
        range_y = round(range_y * 0.9 - 1)
        range_z = round(range_z * 0.9 - 1)

        last_max = sorted(counts, key=lambda a: a[0]+a[1]+a[2])[0]

        print(f"\rcurrent location: {base_x}, {base_y}, {base_z}  current search range: {range_x}, {range_y}, {range_z}", end="")

    print("")
    return distance((0, 0, 0), (base_x, base_y, base_z))


def run():
    data = load_data("Day23.txt")
    nanobots = get_nanobots(data)
    strongest = find_strongest(nanobots)
    in_range = count_in_range_of_bot(strongest, nanobots)
    print(f"The number of nanobots in range of the strongest nanobot is {in_range}")
    dist = find_best_spot_distance(nanobots)
    print(f"The manhattan distance to the closest spot with optimal reach is {dist}")
    # (52018071, 47441514, 24816518, 918) -> 124276103

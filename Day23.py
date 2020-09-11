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


def find_best_spot_distance(nanobots):
    base_x, base_y, base_z = 0, 0, 0
    for exponent in reversed(range(10)):
        counts = []
        for x, y, z in product(range(-5, 5), range(-5, 5), range(-5, 5)):
            bots_in_range = count_in_range_of_point(base_x + x * 10**exponent, base_y + y * 10**exponent, base_z + z * 10**exponent, nanobots)
            counts.append((x, y, z, bots_in_range))
        counts.sort(key=lambda a: a[3], reverse=True)
        best_sector = counts[0]
        base_x += best_sector[0] * 10**exponent
        base_y += best_sector[1] * 10**exponent
        base_z += best_sector[2] * 10**exponent
        print(base_x, base_y, base_z)

    return distance((0, 0, 0), (base_x, base_y, base_z))


def run():
    data = load_data("Day23test.txt")
    nanobots = get_nanobots(data)
    strongest = find_strongest(nanobots)
    in_range = count_in_range_of_bot(strongest, nanobots)
    print(f"The number of nanobots in range of the strongest nanobot is {in_range}")
    dist = find_best_spot_distance(nanobots)
    print(f"The manhattan distance to the closest spot with optimal reach is {dist}")

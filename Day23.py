# AOC18 day 23
from collections import namedtuple


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


def count_in_range_of_strongest(nanobots):
    strongest = nanobots[0]
    for bot in nanobots:
        if bot.r > strongest.r:
            strongest = bot
    in_range = 0
    for bot in nanobots:
        if strongest.r >= (abs(bot.x - strongest.x) + abs(bot.y - strongest.y) + abs(bot.z - strongest.z)):
            in_range += 1
    return in_range


def run():
    data = load_data("Day23.txt")
    nanobots = get_nanobots(data)
    in_range = count_in_range_of_strongest(nanobots)
    print(f"The number of nanobots in range of the strongest nanobot is {in_range}")

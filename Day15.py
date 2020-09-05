# AOC18 day 15
from cave import Cave


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def run():
    # data = load_data("Day15.txt")
    data = load_data("Day15test0.txt")
    cave = Cave(data)
    cave.show()
    outcome = cave.run()
    cave.show()
    print(f"The outcome is {outcome}")

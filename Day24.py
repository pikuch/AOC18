# AOC18 day 24
from infection import Infection


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def run():
    data = load_data("Day24test.txt")
    infection = Infection()
    infection.load_data(data)
    infection.run()


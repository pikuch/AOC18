# AOC18 day 01
from functools import reduce


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def find_frequency(changes):
    return reduce(lambda x, y: x + y, changes, 0)


def find_first_revisited(changes):
    frequencies = set()
    current_frequency = 0
    frequencies.add(0)
    while True:
        for change in changes:
            current_frequency += change
            if current_frequency in frequencies:
                return current_frequency
            else:
                frequencies.add(current_frequency)


def run():
    data = load_data("Day01.txt")
    nums = list(map(int, data.split("\n")))
    frequency = find_frequency(nums)
    print(f"The resulting frequency is {frequency}")
    revisited = find_first_revisited(nums)
    print(f"The first revisited frequency is {revisited}")

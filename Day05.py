# AOC18 day 05
from collections import deque


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def to_numbers(data):
    nums = list(data)
    for i in range(len(nums)):
        if nums[i].isupper():
            nums[i] = ord(nums[i].lower())
        else:
            nums[i] = -ord(nums[i])
    return nums


def to_numbers_without(data, deleted):
    nums = list(data.replace(chr(deleted), "").replace(chr(deleted).upper(), ""))
    for i in range(len(nums)):
        if nums[i].isupper():
            nums[i] = ord(nums[i].lower())
        else:
            nums[i] = -ord(nums[i])
    return nums


def shorten(s):
    unshorted = deque()
    for i in range(len(s)):
        if len(unshorted) == 0:
            unshorted.append(s[i])
        else:
            if s[i] + unshorted[-1] == 0:
                unshorted.pop()
            else:
                unshorted.append(s[i])

    return len(unshorted)


def without_one(data):
    minimum = 10**10
    for deleted in range(ord("a"), ord("z") + 1):
        nums = to_numbers_without(data, deleted)
        short = shorten(nums)
        if short < minimum:
            minimum = short
    return minimum


def run():
    data = load_data("Day05.txt")
    # data = "dabAcCaCBAcCcaDA"
    num_list = to_numbers(data)
    shortened = shorten(num_list)
    print(f"The fully shortened polymer is {shortened} units long")
    shortest = without_one(data)
    print(f"Removing one unit type lets us shorten the polymer to {shortest} units long")

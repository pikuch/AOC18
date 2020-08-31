# AOC18 day 02
from collections import Counter
from itertools import combinations


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def get_checksum(ids):
    count2 = 0
    count3 = 0
    for code in ids:
        counts = Counter(code).values()
        count2 += 2 in counts
        count3 += 3 in counts
    return count2 * count3


def diff_strings(s1, s2):
    diff_count = 0
    index = 0
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            diff_count += 1
            if diff_count > 1:
                return None
            index = i

    if diff_count == 1:
        return s1[:index] + s1[index+1:]


def get_common_letters(data):
    for s in combinations(data, 2):
        if (diff := diff_strings(*s)) is not None:
            return diff


def run():
    data = load_data("Day02.txt").split("\n")
    checksum = get_checksum(data)
    print(f"The checksum is {checksum}")
    common = get_common_letters(data)
    print(f"The common letters are {common}")

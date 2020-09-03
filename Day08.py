# AOC18 day 08
from collections import deque, defaultdict


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def sum_metadata(data):
    meta_sum = 0
    to_check = deque()
    to_check.append(data[1])
    to_check.extend(["c"] * data[0])
    pos = 2
    while len(to_check):
        current = to_check.pop()
        if current == "c":
            to_check.append(data[pos + 1])
            to_check.extend(["c"] * data[pos])
            pos += 2
        else:
            meta_sum += sum(data[pos: pos + current])
            pos += current
    return meta_sum


def sum_values(data):
    to_check = deque()
    to_check.append((data[1], 0))
    for _ in range(data[0]):
        to_check.append(("c", 0))
    outputs = defaultdict(lambda: [])
    pos = 2
    while len(to_check):
        current, depth = to_check.pop()
        if current == "c":
            to_check.append((data[pos + 1], depth + 1))
            for _ in range(data[pos]):
                to_check.append(("c", depth + 1))
            pos += 2
        else:
            if len(outputs[depth]):  # has children
                sum_kids = 0
                for i in range(current):
                    if data[pos + i] - 1 < len(outputs[depth]):
                        sum_kids += outputs[depth][data[pos + i] - 1]
                outputs[depth - 1].append(sum_kids)
                pos += current
                outputs[depth] = []
            else:
                outputs[depth - 1].append(sum(data[pos: pos + current]))
                pos += current

    return outputs[-1][0]


def run():
    data = list(map(int, load_data("Day08.txt").split()))
    print(f"The sum of metadata entries is {sum_metadata(data)}")
    print(f"The value of the root is {sum_values(data)}")

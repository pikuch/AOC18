# AOC18 day 03
from collections import namedtuple


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def make_square(s):
    Rect = namedtuple("Rect", ("id", "x0", "y0", "x1", "y1"))
    words = tuple(map(int, s.translate(str.maketrans("#@,:x", "     ")).split()))
    return Rect(words[0], words[1] + 1, words[2] + 1, words[1] + words[3], words[2] + words[4])


def count_overlaps(rectangles):
    inches = {}
    for rect in rectangles:
        for x in range(rect.x0, rect.x1 + 1):
            for y in range(rect.y0, rect.y1 + 1):
                if (x, y) in inches:
                    inches[(x, y)] += 1
                else:
                    inches[(x, y)] = 1
    return sum([1 for v in inches.values() if v > 1])


def find_not_overlapping(rectangles):
    overlapped = set()
    inches = {}
    for rect in rectangles:
        for x in range(rect.x0, rect.x1 + 1):
            for y in range(rect.y0, rect.y1 + 1):
                if (x, y) in inches:
                    overlapped.add(rect.id)
                    overlapped.add(inches[(x, y)])
                else:
                    inches[(x, y)] = rect.id
    for rect in rectangles:
        if rect.id not in overlapped:
            return rect.id


def run():
    data = load_data("Day03.txt").split("\n")
    rectangles = list(map(make_square, data))
    overlaps = count_overlaps(rectangles)
    print(f"There are {overlaps} overlapping inches")
    claim = find_not_overlapping(rectangles)
    print(f"Claim {claim} is not overlapping")

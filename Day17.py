# AOC18 day 17
from collections import deque
from PIL import Image, ImagePalette
import numpy as np


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def make_scan(data):
    min_y = 9**9
    max_x = 0
    max_y = 0
    areas = []
    for line in data.split("\n"):
        words = line.translate(str.maketrans("=,.", "   ")).split()
        words[1] = int(words[1])
        words[3] = int(words[3])
        words[4] = int(words[4])
        areas.append(words)
        if words[0] == "x":
            if words[1] > max_x:
                max_x = words[1]
            if words[4] > max_y:
                max_y = words[4]
            if words[3] < min_y:
                min_y = words[3]
        else:
            if words[4] > max_x:
                max_x = words[4]
            if words[1] > max_y:
                max_y = words[1]
            if words[1] < min_y:
                min_y = words[1]
    scan = np.zeros((max_y + 1, max_x + 1), dtype=np.uint8)
    for area in areas:
        if area[0] == "x":
            scan[area[3]:area[4]+1, area[1]] = 1
        else:
            scan[area[1], area[3]:area[4]+1] = 1
    return scan, min_y


def show(scan, place=None):
    rrrgggbbb = [40, 160, 50, 50,
                 20, 160, 150, 100,
                 0, 160, 250, 150]
    pal = ImagePalette.ImagePalette("RGB", rrrgggbbb, 12)
    if place is None:
        img = Image.fromarray(scan, mode="P")
    else:
        img = Image.fromarray(scan[max(0, place[0]-place[2]):min(scan.shape[0]-1, place[0]+place[2]),
                                   max(0, place[1]-place[3]):min(scan.shape[1]-1, place[1]+place[3])], mode="P")
        img = img.resize((img.size[0]*10, img.size[1]*10))
    img.putpalette(pal)
    img.show()


def water_fill(scan):
    EMPTY, WALL, FLOW, STILL = 0, 1, 2, 3
    streams = deque()
    streams.append((1, 500))
    while len(streams):
        r, c = streams.pop()
        if r + 1 >= scan.shape[0]:
            scan[r, c] = FLOW
            continue
        if scan[r, c] == STILL:
            continue
        below = scan[r + 1, c]
        if below == EMPTY:
            scan[r, c] = FLOW
            streams.append((r + 1, c))
        elif below == FLOW:
            scan[r, c] = FLOW
        elif scan[r + 1, c] == WALL or scan[r + 1, c] == STILL:
            # detect left and right limits
            dcl = 0
            while (scan[r+1, c+dcl] == WALL or scan[r+1, c+dcl] == STILL) and (scan[r, c+dcl] == EMPTY or scan[r, c+dcl] == FLOW):
                dcl -= 1
            dcr = 0
            while (scan[r+1, c+dcr] == WALL or scan[r+1, c+dcr] == STILL) and (scan[r, c+dcr] == EMPTY or scan[r, c+dcr] == FLOW):
                dcr += 1

            left = scan[r, c+dcl]
            right = scan[r, c+dcr]
            if (left == EMPTY or left == FLOW) and (right == EMPTY or right == FLOW):  # open on both sides
                scan[r, c+dcl:c+dcr+1] = FLOW
                streams.append((r+1, c+dcl))
                streams.append((r+1, c+dcr))
            elif (left == EMPTY or left == FLOW) and right != EMPTY:  # open on the left
                scan[r, c+dcl:c+dcr] = FLOW
                streams.append((r+1, c+dcl))
            elif left != EMPTY and (right == EMPTY or right == FLOW):  # open on the right
                scan[r, c+dcl+1:c+dcr+1] = FLOW
                streams.append((r+1, c+dcr))
            elif left != EMPTY and right != EMPTY:  # closed on both sides
                scan[r, c+dcl+1:c+dcr] = STILL
                streams.append((r-1, c))


def run():
    data = load_data("Day17.txt")
    scan, min_y = make_scan(data)
    water_fill(scan)
    print(f"The number of wet tiles is {np.sum(scan==2) + np.sum(scan==3) - min_y + 1}")
    print(f"There are {np.sum(scan==3)} stationary water tiles")
    # show(scan)

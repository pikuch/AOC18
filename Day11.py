# AOC18 day 11
import numpy as np


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def square_power(x, y, serial):
    return ((((x + 10) * ((x + 10) * y + serial)) // 100) % 10) - 5


def ask_summed_area(x, y, size, s_a_grid):
    return s_a_grid[x+size-1, y+size-1] - s_a_grid[x+size-1, y-1] - s_a_grid[x-1, y+size-1] + s_a_grid[x-1, y-1]


def generate_summed_area_table(serial):
    grid = np.fromfunction(lambda x, y: square_power(x, y, serial), (301, 301), dtype=np.int32)
    grid[0, :] = 0
    grid[:, 0] = 0
    return grid.cumsum(axis=0).cumsum(axis=1)


def find_coords_3x3(s_a_grid):
    max_area = -9**9
    mx, my = 0, 0
    for x in range(1, 298):
        for y in range(1, 298):
            area = ask_summed_area(x, y, 3, s_a_grid)
            if area > max_area:
                max_area = area
                mx = x
                my = y
    return str(mx)+","+str(my)


def find_coords_any_size(s_a_grid):
    max_area = -9**9
    mx, my, msize = 0, 0, 0
    for size in range(1, 301):
        for x in range(1, 301-size):
            for y in range(1, 301-size):
                area = ask_summed_area(x, y, size, s_a_grid)
                if area > max_area:
                    max_area = area
                    mx = x
                    my = y
                    msize = size
    return str(mx)+","+str(my)+","+str(msize)


def run():
    data = load_data("Day11.txt")
    serial = int(data)
    grid = generate_summed_area_table(serial)
    print(f"The coordinates of the 3x3 square with the maximum power level are {find_coords_3x3(grid)}")
    print(f"The coordinates of the square of any size with the maximum power level are {find_coords_any_size(grid)}")

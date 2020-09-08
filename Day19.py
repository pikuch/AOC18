# AOC18 day 19
from theDeviceV2 import DeviceV2
from math import sqrt, ceil


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def sum_of_divisors(n):
    s = 0
    for i in range(1, n+1):
        if n % i == 0:
            s += i
    return s


def run():
    data = load_data("Day19.txt")
    # device = DeviceV2()
    # device.load(data)
    # device.run()
    # print(f"Register 0 after the run: {device.reg[0]}")

    # device = DeviceV2()
    # device.load(data)
    # device.reg[0] = 1
    # for line in device.translate():
    #     print(line)

    # the device sums the divisors of 1017 (r0 = 0) or 10551417 (r0 = 1)
    print(sum_of_divisors(1017))
    print(sum_of_divisors(10551417))

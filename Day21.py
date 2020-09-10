# AOC18 day 21
from theDeviceV2_catch_eq import DeviceV2_catch_eq


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def run():
    data = load_data("Day21.txt")
    device = DeviceV2_catch_eq()
    device.load(data)
    device.run()
    # the result:
    # The first value is 11592302
    # looking for a cycle... 15600
    # The last stopping value is 313035

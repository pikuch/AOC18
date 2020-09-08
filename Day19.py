# AOC18 day 19
from theDeviceV2 import DeviceV2


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def run():
    data = load_data("Day19.txt")
    device = DeviceV2()
    device.load(data)
    device.run()
    print(f"Register 0 after the run: {device.reg[0]}")

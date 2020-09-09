# AOC18 day 21
from theDeviceV2 import DeviceV2


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def run():
    data = load_data("Day21.txt")
    device = DeviceV2()
    device.load(data)
    device.run()
    # part 1:
    # 11592302 - found by catching the eqrr 1 0 5 instruction
    # part 2:


    # in the device:
    # reg_1_values = set()
    # last_reg_1 = 0
    #
    #     if inst[0] == "eqrr":
    #         print(f"\r{len(reg_1_values)}", end="")
    #         if self.reg[1] in reg_1_values:
    #             print(last_reg_1)
    #             break
    #         else:
    #             reg_1_values.add(self.reg[1])
    #             last_reg_1 = self.reg[1]
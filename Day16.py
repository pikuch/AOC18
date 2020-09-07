# AOC18 day 16
from theDevice import Device


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def parse_data(data):
    tests = []
    items = data.split("\n\n")
    i = 0
    while True:
        if len(items[i]) == 0:
            break
        lines = items[i].split("\n")
        before = tuple(map(int, lines[0][8:].translate(str.maketrans("[,]", "   ")).split()))
        operation = tuple(map(int, lines[1].split()))
        after = tuple(map(int, lines[2][8:].translate(str.maketrans("[,]", "   ")).split()))
        tests.append(tuple([before, operation, after]))
        i += 1

    program = []
    for line in items[-1].split("\n"):
        program.append(tuple(map(int, line.split())))

    return tests, program


def how_many_tests_fit_3_or_more_ops(tests):
    device = Device()
    count_3_plus = 0
    for test in tests:
        if device.count_fitting_operations(test[0], test[1], test[2]) >= 3:
            count_3_plus += 1
    device.figure_out_the_opcodes()
    opcode_changes = ""
    for code in device.possible_opcodes:
        opcode_changes += f"[{list(device.possible_opcodes[code])[0]} -> {code}] "
    return count_3_plus, opcode_changes


def run():
    data = load_data("Day16.txt")
    tests, program = parse_data(data)
    fitting_at_least_3, opcodes = how_many_tests_fit_3_or_more_ops(tests)
    print(f"{fitting_at_least_3} samples behave like 3 or more opcodes")
    print(f"Needed opcode changes are: {opcodes}")
    device = Device()
    device.load(program)
    device.run()
    print(f"Register 0 contains {device.reg[0]} after running the program")

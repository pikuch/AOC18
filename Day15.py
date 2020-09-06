# AOC18 day 15
from cave import Cave


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def run():
    data = load_data("Day15.txt")
    cave = Cave(data, 3)
    cave.show()
    outcome, elf_deaths = cave.run()
    print(f"The outcome is {outcome}")
    # part 2
    elf_ap = 4
    elf_deaths = 1
    while elf_deaths:
        cave = Cave(data, elf_ap)
        outcome, elf_deaths = cave.run()
        print(f"The elf ap of {elf_ap} leaves {elf_deaths} elves dead")
        elf_ap += 1
    print(f"The outcome is {outcome}")

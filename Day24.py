# AOC18 day 24
from infection import Infection


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def run():
    data = load_data("Day24.txt")
    infection = Infection()
    infection.load_data(data, 0)
    outcome_immune, outcome_infection = infection.run()
    print(f"The immune system is left with {outcome_immune} units while the infection has {outcome_infection}")

    # part 2
    boost = 0
    outcome_immune = 0
    while outcome_infection:
        boost += 1
        infection = Infection()
        infection.load_data(data, boost)
        outcome_immune, outcome_infection = infection.run()
        print(f"boost: {boost}\t immune: {outcome_immune}\t infection:{outcome_infection}")
    print(f"The smallest effective immune system boost is {boost} and it leaves the immune system with {outcome_immune} units")

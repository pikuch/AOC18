# AOC18 day 14

def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def try_recipes(n):
    recipes = [3, 7]
    elf1 = 0
    elf2 = 1
    while len(recipes) < n+10:
        recipes.extend(map(int, list(str(recipes[elf1] + recipes[elf2]))))
        elf1 = (elf1 + recipes[elf1] + 1) % len(recipes)
        elf2 = (elf2 + recipes[elf2] + 1) % len(recipes)
    return "".join(map(str, recipes[n:n+10]))


def count_digits(n):
    list_n = list(map(int, list(str(n))))
    len_n = len(list_n)
    recipes = [3, 7]
    elf1 = 0
    elf2 = 1
    while True:
        new_recipes = list(map(int, list(str(recipes[elf1] + recipes[elf2]))))
        for r in new_recipes:
            recipes.append(r)
            if recipes[-len_n:] == list_n:
                return len(recipes) - len_n

        elf1 = (elf1 + recipes[elf1] + 1) % len(recipes)
        elf2 = (elf2 + recipes[elf2] + 1) % len(recipes)


def run():
    data = load_data("Day14.txt")
    n_recipes = int(data)
    print(f"The next 10 digits are: {try_recipes(n_recipes)}")
    print(f"There are {count_digits(n_recipes)} digits to the left")

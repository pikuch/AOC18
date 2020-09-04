# AOC18 day 12


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def parse_input(data):
    state = [0, 0, 0, 0]
    rules = {}
    words = data[0].split()
    for i in range(len(words[2])):
        if words[2][i] == ".":
            state.append(0)
        else:
            state.append(1)
    state.extend([0, 0, 0, 0])

    for line in data[2:]:
        words = line.split()
        bits = [0 if words[0][pos] == "." else 1 for pos in range(5)]
        rules[tuple(bits)] = 0 if words[2] == "." else 1
    return state, rules


def get_rule(state, i, rules):
    pattern = tuple(state[i - 2:i + 3])
    if pattern in rules:
        return rules[pattern]
    else:
        return 0


def sum_after(state, rules, generations):
    track_start = -4
    for n in range(generations):
        new_state = []
        for i in range(2, len(state) - 3):
            new_state.append(get_rule(state, i, rules))
        i0 = 0
        while not new_state[i0]:
            i0 += 1
        i1 = len(new_state) - 1
        while not new_state[i1]:
            i1 -= 1
        state = [0] * 4 + new_state[i0:i1+1] + [0] * 4
        track_start += i0 - 2
    sum_plants = 0
    for i in range(len(state)):
        if state[i]:
            sum_plants += i + track_start
    return sum_plants


def sum_after_shortcut(state, rules, generations):
    old_states = {}
    track_start = -4
    n = 0
    while n < generations:
        n += 1
        new_state = []
        for i in range(2, len(state) - 3):
            new_state.append(get_rule(state, i, rules))
        i0 = 0
        while not new_state[i0]:
            i0 += 1
        i1 = len(new_state) - 1
        while not new_state[i1]:
            i1 -= 1
        state = [0] * 4 + new_state[i0:i1 + 1] + [0] * 4
        track_start += i0 - 2
        if tuple(state) in old_states:
            prev_n, prev_track_start = old_states[tuple(state)]
            missing_n = (generations - n) // (n-prev_n)
            missing_track_start = missing_n * (track_start - prev_track_start)
            n += missing_n
            track_start += missing_track_start
        else:
            old_states[tuple(state)] = (n, track_start)
    sum_plants = 0
    for i in range(len(state)):
        if state[i]:
            sum_plants += i + track_start
    return sum_plants


def run():
    data = load_data("Day12.txt").split("\n")
    state, rules = parse_input(data)
    print(f"After 20 generations the sum of numbers of pots is {sum_after(state, rules, 20)}")
    print(f"After 5*10^10 generations the sum of numbers of pots is {sum_after_shortcut(state, rules, 5*(10**10))}")

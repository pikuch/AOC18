# AOC18 day 07
from collections import defaultdict


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def parse_data(data):
    steps = defaultdict(lambda: set())
    for line in data.split("\n"):
        words = line.split()
        steps[words[7]].add(words[1])
        if words[1] not in steps:
            steps[words[1]] = set()
    return steps


def order_steps(steps):
    ordered = []
    ready = []
    for step, prerequisites in steps.items():
        if len(prerequisites) == 0:
            ready.append(step)
            prerequisites.add("-")
    while len(ready):
        ready.sort(reverse=True)
        chosen = ready.pop(-1)
        ordered.append(chosen)
        for step, prerequisites in steps.items():
            if chosen in prerequisites:
                prerequisites.remove(chosen)
            if len(prerequisites) == 0:
                ready.append(step)
                prerequisites.add("-")

    return "".join(ordered)


def build_together(steps):
    t = 0
    ordered = []
    ready = []
    workers = []
    for step, prerequisites in steps.items():
        if len(prerequisites) == 0:
            ready.append(step)
            prerequisites.add("-")
    while len(ready) or len(workers):
        # finish jobs
        for w in reversed(range(len(workers))):
            if workers[w][1] == 0:
                item = workers[w][0]
                del workers[w]
                for step, prerequisites in steps.items():
                    if item in prerequisites:
                        prerequisites.remove(item)
                    if len(prerequisites) == 0:
                        ready.append(step)
                        prerequisites.add("-")

        # add new jobs
        ready.sort(reverse=True)
        for i in range(min(5 - len(workers), len(ready))):
            item = ready.pop(-1)
            workers.append([item, 61 + ord(item) - ord("A")])

        # do jobs
        for work in workers:
            work[1] -= 1
        t += 1

    return t-1


def run():
    data = load_data("Day07.txt")
    steps = parse_data(data)
    order = order_steps(steps)
    print(f"The instructions should be completed in order {order}")
    steps = parse_data(data)
    job_time = build_together(steps)
    print(f"The steps will take 5 people {job_time} seconds")

# AOC18 day 04
from datetime import datetime, timedelta
from collections import defaultdict


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def construct_records(data):
    sleeping = defaultdict(lambda: {})
    guards = {}
    records = {}
    for line in data:
        words = line.split()
        date = datetime.strptime(words[0], "[%Y-%m-%d")
        if words[1][0] != "0":  # move date a day forward
            date = date + timedelta(days=1)
        if words[2] == "Guard":
            guards[date] = int(words[3][1:])
            sleeping[date][-1] = 0  # so that record exists even without sleeping
        else:
            if words[2] == "falls":
                sleeping[date][int(words[1][3:5])] = 1
            else:
                sleeping[date][int(words[1][3:5])] = 0

    for date in guards.keys():
        records[date] = []

    for date, changes in sleeping.items():
        current = 0
        for i in range(60):
            if i in sleeping[date]:
                current = sleeping[date][i]
            records[date].append(current)
    return guards, records


def strategy1(guards, records):
    sleep_counter = defaultdict(lambda: 0)
    for day, schedule in records.items():
        sleep_counter[guards[day]] += sum(schedule)
    sleepy_id = sorted(list(sleep_counter.items()), key=lambda x: x[1], reverse=True)[0][0]
    minute_counter = [0] * 60
    for day, schedule in records.items():
        if guards[day] == sleepy_id:
            for i in range(60):
                minute_counter[i] += schedule[i]
    sleepy_minute = minute_counter.index(max(minute_counter))
    return sleepy_id, sleepy_minute


def strategy2(guards, records):
    sleepy_id = 0
    times_asleep = 0
    sleepy_minute = 0
    for guard in guards.values():
        minute_counter = [0] * 60
        for day, schedule in records.items():
            if guards[day] == guard:
                for i in range(60):
                    minute_counter[i] += schedule[i]
        max_asleep = max(minute_counter)
        if max_asleep > times_asleep:
            times_asleep = max_asleep
            sleepy_id = guard
            sleepy_minute = minute_counter.index(max_asleep)
    return sleepy_id, sleepy_minute


def run():
    data = load_data("Day04.txt").split("\n")
    guards, records = construct_records(data)
    guard_id, sleepy_minute = strategy1(guards, records)
    print(f"The most sleeping guard multiplied by his most sleepy minute is {guard_id * sleepy_minute}")
    guard_id, sleepy_minute = strategy2(guards, records)
    print(f"The most sleeping guard on the same minute times his most sleepy minute is {guard_id * sleepy_minute}")

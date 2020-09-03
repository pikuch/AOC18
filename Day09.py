# AOC18 day 09
from node import Node


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def parse_input(data):
    words  = data.split()
    return int(words[0]), int(words[6])


def calculate_quick(player_count, last_marble):
    scores = [0] * player_count
    marbles = Node(0)
    for m in range(1, last_marble + 1):
        if m % 23 == 0:
            for _ in range(7):
                marbles = marbles.prev
            val7 = marbles.val
            marbles = marbles.remove()
            scores[m % player_count] += m + val7
        else:
            marbles = marbles.next
            marbles = marbles.insert_after(m)
    return max(scores)


def run():
    data = load_data("Day09.txt")
    player_count, last_marble = parse_input(data)
    print(f"The winning score is {calculate_quick(player_count, last_marble)}")
    print(f"The winning score for 100 times more marbles is {calculate_quick(player_count, last_marble * 100)}")

# AOC18 day 20
from collections import deque


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def make_rooms(re):
    max_moves = 0
    at_least_1k = 0
    rooms = {(0, 0): 0}
    move_x = {"N": 0, "S": 0, "E": 1, "W": -1}
    move_y = {"N": -1, "S": 1, "E": 0, "W": 0}
    x, y, moves = 0, 0, 0
    to_check = []
    for i in range(1, len(re)-1):
        if re[i] == "(":
            to_check.append((x, y, moves))
        elif re[i] == ")":
            x, y, moves = to_check.pop()
        elif re[i] == "|":
            x, y, moves = to_check[-1]
        else:
            x += move_x[re[i]]
            y += move_y[re[i]]
            moves += 1
            if (x, y) not in rooms:
                rooms[(x, y)] = moves
                if moves >= 1000:
                    at_least_1k += 1
            else:
                moves = rooms[(x, y)]
            if moves > max_moves:
                max_moves = moves

    return rooms, max_moves, at_least_1k


def run():
    data = load_data("Day20.txt")
    # test data
    # data = "^WNE$"  # result == 3
    # data = "^ENWWW(NEEE|SSE(EE|N))$"  # result == 10
    # data = "^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$"  # result == 18
    # data = "^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$"  # result == 23
    # data = "^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$"  # result == 31
    rooms, max_dist, at_least_1k = make_rooms(data)
    print(f"The most distant room is {max_dist} doors away and there are {at_least_1k} rooms at least 1000 doors away")

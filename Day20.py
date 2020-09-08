# AOC18 day 20


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def run():
    data = load_data("Day20.txt")
    # test data
    data = "^WNE$"  # result == 3
    # data = "^ENWWW(NEEE|SSE(EE|N))$"  # result == 10
    # data = "^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$"  # result == 18
    # data = "^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$"  # result == 23
    # data = "^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$"  # result == 31


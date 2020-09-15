# AOC18 day 25


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def parse_points(data):
    points = []
    lines = data.split("\n")
    for line in lines:
        points.append(tuple(map(int, line.split(","))))
    return points


def dist(p0, p1):
    return abs(p1[0] - p0[0]) + abs(p1[1] - p0[1]) + abs(p1[2] - p0[2]) + abs(p1[3] - p0[3])


def in_constellation(point, constellation):
    for c_point in constellation:
        if dist(point, c_point) <= 3:
            return True
    return False


def make_constellations(points):
    constellations = [[points[0]]]
    for p in points[1:]:
        part_of = []
        for c in range(len(constellations)):
            if in_constellation(p, constellations[c]):
                part_of.append(c)
        if len(part_of) == 0:
            constellations.append([p])
        elif len(part_of) == 1:
            constellations[part_of[0]].append(p)
        else:
            constellations[part_of[0]].append(p)
            for to_join in reversed(part_of[1:]):
                constellations[part_of[0]].extend(constellations[to_join])
                del constellations[to_join]

    return constellations


def run():
    data = load_data("Day25.txt")
    points = parse_points(data)
    constellations = make_constellations(points)
    print(f"There are {len(constellations)} constellations!")
    # for c in constellations:
    #     print(c)

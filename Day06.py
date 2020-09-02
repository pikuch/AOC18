# AOC18 day 06
from collections import namedtuple, deque


def load_data(f_name):
    with open(f_name, "r") as f:
        data_read = f.read()
    return data_read


def parse_points(data):
    Point = namedtuple("Point", ["x", "y"])
    points = []
    for p in data.split("\n"):
        words = p.split(",")
        points.append(Point(int(words[0]), int(words[1])))
    return points


def is_on_the_edge(p, points):
    is_edge = [1] * 4
    for i in range(len(points)):
        if i != p:
            if points[i].y < points[p].y and abs(points[p].x - points[i].x) < points[p].y - points[i].y:
                is_edge[0] = 0
            if points[i].y > points[p].y and abs(points[p].x - points[i].x) < points[i].y - points[p].y:
                is_edge[1] = 0
            if points[i].x < points[p].x and abs(points[p].y - points[i].y) < points[p].x - points[i].x:
                is_edge[2] = 0
            if points[i].x > points[p].x and abs(points[p].y - points[i].y) < points[i].x - points[p].x:
                is_edge[3] = 0
    if sum(is_edge):
        return True
    else:
        return False


def find_closest_to(x, y, points):
    closest = -1
    distance = 9**9
    was_equal = False
    for p in range(len(points)):
        current_distance = abs(points[p].x - x) + abs(points[p].y - y)
        if current_distance < distance:
            distance = current_distance
            closest = p
            was_equal = False
        elif current_distance == distance:
            was_equal = True
        else:
            pass
    if was_equal:
        return None
    else:
        return closest


def get_spread(points):
    min_x = min_y = 9 ** 9
    max_x = max_y = 0
    for p in range(len(points)):
        if points[p].x < min_x:
            min_x = points[p].x
        if points[p].x > max_x:
            max_x = points[p].x
        if points[p].y < min_y:
            min_y = points[p].y
        if points[p].y > max_y:
            max_y = points[p].y
    return min_x, min_y, max_x, max_y


def find_largest_area(min_x, min_y, max_x, max_y, points):
    internal = {}
    for p in range(len(points)):
        if not is_on_the_edge(p, points):
            internal[p] = 0

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            closest_id = find_closest_to(x, y, points)
            if closest_id in internal:
                internal[closest_id] += 1

    areas = sorted(internal.items(), key=lambda a: a[1], reverse=True)
    return areas[0][1]


def sum_distances(x, y, points):
    sum_dist = 0
    for p in range(len(points)):
        sum_dist += abs(points[p].x - x) + abs(points[p].y - y)
    return sum_dist


def find_area_close_to_all(min_x, min_y, max_x, max_y, points):
    within_10k = 0
    visited = set()
    to_check = deque()
    to_check.append(((max_x-min_x)//2, (max_y-min_y)//2))
    visited.add(((max_x-min_x)//2, (max_y-min_y)//2))

    while len(to_check):
        x, y = to_check.popleft()
        sum_dist = sum_distances(x, y, points)
        if sum_dist < 10000:
            within_10k += 1
            if (x-1, y) not in visited:
                to_check.append((x-1, y))
                visited.add((x-1, y))
            if (x+1, y) not in visited:
                to_check.append((x+1, y))
                visited.add((x+1, y))
            if (x, y-1) not in visited:
                to_check.append((x, y-1))
                visited.add((x, y-1))
            if (x, y+1) not in visited:
                to_check.append((x, y+1))
                visited.add((x, y+1))
    return within_10k


def run():
    data = load_data("Day06.txt")
    points = parse_points(data)
    min_x, min_y, max_x, max_y = get_spread(points)
    largest = find_largest_area(min_x, min_y, max_x, max_y, points)
    print(f"The largest finite area is {largest} square units")
    area_close = find_area_close_to_all(min_x, min_y, max_x, max_y, points)
    print(f"The area of points closer than 10000 to all points is {area_close}")

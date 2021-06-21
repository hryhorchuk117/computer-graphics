import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import math


def calculate_side(point1, point2) -> float:
    return math.sqrt(math.pow(point1[0] - point2[0], 2) + math.pow(point1[1] - point2[1], 2))


def triangle_area(point, line_start, line_end) -> float:
    if line_start == line_end:
        line_end = [line_start[0], line_start[1] + 1000]
    a = calculate_side(point, line_start)
    b = calculate_side(point, line_end)
    c = calculate_side(line_start, line_end)
    p = (a + b + c) / 2
    return math.sqrt(p * (p - a) * (p - b) * (p - c))


def is_left_or_on(point, line_start, line_end) -> bool:
    return (line_end[0] - line_start[0]) * (point[1] - line_start[1]) \
           - (line_end[1] - line_start[1]) * (point[0] - line_start[0]) >= 0


def find_farthest_point(points, line_start, line_end):
    distance = -1
    result = [0, 0]
    for point in points:
        next_distance = triangle_area(point, line_start, line_end)
        if next_distance > distance:
            distance = next_distance
            result = point
    return result


def points_lefter(points, line_start, line_end):
    answer = []
    for point in points:
        if is_left_or_on(point, line_start, line_end):
            answer.append(point)
    return answer


def quick_hull(points, start, end):
    if len(points) == 0:
        return []
    if points == [start, end]:
        return [start, end]
    elif points == [end, start]:
        return [start, end]
    elif points == [start]:
        return [start]
    elif points == [end]:
        return [end]
    else:
        farthest_point = find_farthest_point(points, start, end)
        if farthest_point == start or farthest_point == end:
            return [start, end]
        point_for_left = points_lefter(points, start, farthest_point)
        points_for_right = points_lefter(points, farthest_point, end)
        return quick_hull(point_for_left, start, farthest_point) + quick_hull(points_for_right, farthest_point, end)


def entry_point(points):
    result = points[0]
    for point in points:
        if point[0] < result[0]:
            result = point
    return result


def read_points(file):
    points = []
    input_data = open(file).read().split()

    i = 0
    while i < len(input_data):
        points.append([float(input_data[i]), float(input_data[i + 1])])
        i += 2

    return points


def draw(points, quick_hull):
    fig, ax = plt.subplots()
    ax.set_xlim([-10, 15])
    ax.set_ylim([-10, 15])

    for point in points:
        plt.scatter(point[0], point[1], s=10, edgecolors='g', facecolor='g')

    lines = [[quick_hull[len(quick_hull) - 1], quick_hull[0]]]
    for i in range(1, len(quick_hull)):
        lines.append([quick_hull[i - 1], quick_hull[i]])
    lc = LineCollection(lines, linewidths=1)
    ax.add_collection(lc)

    plt.show()


def main():
    points = read_points("points.txt")
    entry = entry_point(points)
    quick_hull_result = quick_hull(points, entry, entry)
    draw(points, quick_hull_result)


if __name__ == "__main__":
    main()

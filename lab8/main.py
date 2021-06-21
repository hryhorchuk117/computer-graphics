import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

eps = 0.00001

TURN_LEFT, TURN_RIGHT, TURN_NONE = (1, -1, 0)


def turn(p, q, r):
    angle = (q[0] - p[0])*(r[1] - p[1]) - (r[0] - p[0])*(q[1] - p[1])
    if angle > 0:
        return TURN_LEFT
    elif angle < 0:
        return TURN_RIGHT
    return TURN_NONE


def distance(p, q):
    dx, dy = q[0] - p[0], q[1] - p[1]
    return dx * dx + dy * dy


def next_point(points, p):
    next_p = p
    for curr_point in points:
        t = turn(p, next_p, curr_point)
        if t == TURN_RIGHT or t == TURN_NONE and distance(p, curr_point) > distance(p, next_p):
            next_p = curr_point
    return points.index(next_p)


def area(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def left_most(candidates):
    i = 0
    res_i = 0
    res = candidates[0]
    for p in candidates:
        if p[0] < res[0]:
            res = p
            res_i = i
        i += 1
    return res, res_i


def right_most(candidates):
    i = 0
    res_i = 0
    res = candidates[0]
    for p in candidates:
        if p[0] > res[0]:
            res = p
            res_i = i
        i += 1
    return res, res_i


def left(a, b, c) -> bool:
    return area(a, b, c) > 0


def simple_polygon_hull(vertexes):
    q0, left_ind = left_most(vertexes)
    qm, right_ind = right_most(vertexes)

    Q = get_chain_hull(vertexes, left_ind, right_ind) + get_chain_hull(vertexes, right_ind, left_ind)

    return Q


def get_chain_hull(chain, left_ind, right_ind):
    half_hull = []
    first = chain[left_ind]

    dummyNode = [first[0], first[1] - eps]
    half_hull.append(dummyNode)
    half_hull.append(first)

    i = left_ind
    while i != right_ind:
        next_to_peek = half_hull[len(half_hull) - 2]
        curr_node = chain[i]

        if not left(next_to_peek, curr_node, half_hull[len(half_hull) - 1]):
            if left(chain[right_ind], half_hull[len(half_hull) - 1], curr_node) or i == right_ind:
                half_hull.append(curr_node)
            i = next_point(chain, curr_node)
        else:
            half_hull.pop()

    return half_hull


def read_points(file):
    points = []
    input_data = open(file).read().split()

    i = 0
    while i < len(input_data):
        points.append([float(input_data[i]), float(input_data[i + 1])])
        i += 2

    return points


def draw(points, result):
    fig, ax = plt.subplots()
    ax.set_xlim([-10, 15])
    ax.set_ylim([-10, 15])

    for point in points:
        plt.scatter(point[0], point[1], s=10, edgecolors='m', facecolor='c')

    lines = [[result[len(result) - 1], result[0]]]
    for i in range(1, len(result)):
        lines.append([result[i - 1], result[i]])
    lc = LineCollection(lines, linewidths=1)
    ax.add_collection(lc)

    plt.show()


points = read_points("points.txt")
result = simple_polygon_hull(points)

draw(points, result)
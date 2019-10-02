import math


def distance(p1, p2):
    dx = p1["x"] - p2["x"]
    dy = p1["y"] - p2["y"]
    return math.sqrt(dx * dx + dy * dy)


def swap(lst, x, y):
    lst[x], lst[y] = lst[y], lst[x]


def next_of_list(lst, index):
    return lst[(index + 1) % len(lst)]


def pre_of_list(lst, index):
    return lst[(index - 1) % len(lst)]

import math


def ucb1(sn: int, n: int, w: float) -> float:
    return -w / n + (2 * math.log(sn) / n) ** 0.5


def argmax(collection) -> int:
    return collection.index(max(collection))


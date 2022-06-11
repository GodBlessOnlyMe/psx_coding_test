"""
생각한 점
- increment function을 도입함으로써 pingpong 함수의 stack 지수적 증가를 방지
- default stack size 1000보다 이상을 요구하는 x에 대해서는 sys.setrecursionlimit 을 늘려줘야한다.
"""


def is_multiple_of_seven(x):
    if x % 7 == 0:
        return True


def contains_seven(x):
    if x < 0:
        return contains_seven(-x)
    if x == 0:
        return False
    elif x > 0:
        if x % 10 == 7:
            return True
        if x < 10:
            return False
        return contains_seven(x // 10)


def increment(x):
    if x == 1:
        return 1
    if is_multiple_of_seven(x - 1) or contains_seven(x - 1):
        return (-1 * increment(x - 1))
    else:
        return increment(x - 1)


def pingpong(x):
    if x == 1:
        return 1
    if x == 2:
        return 2
    if is_multiple_of_seven(x - 1) or contains_seven(x - 1):
        return pingpong(x - 2)
    else:
        return pingpong(x - 1) + increment(x)


if __name__ == "__main__":
    assert pingpong(8) == 6
    assert pingpong(22) == 0
    assert pingpong(68) == 2
    assert pingpong(100) == 2

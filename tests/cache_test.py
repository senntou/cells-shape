import os
from mycache.sqlite_cache import cache_to_sqlite


@cache_to_sqlite
def simple_calculate(a: float, b: float) -> tuple[float, float, float, float]:
    return a + b, a - b, a * b, a / b


@cache_to_sqlite
def return_value(a: float) -> float:
    return a


TEST_CASES = [
    (1, 2),
    (3, 4),
    (5, 6),
    (7, 8),
    (9, 10),
]


def test_cache():
    # 1度目の実行、キャッシュに保存される
    for a, b in TEST_CASES:
        simple_calculate(a, b)

    # 2度目の実行、キャッシュから取得される
    for a, b in TEST_CASES:
        result = simple_calculate(a, b)
        assert result == (a + b, a - b, a * b, a / b), f"Failed for {a}, {b}"


def test_float_cache():
    a = 0.0000000000000000001

    # 1度目の実行、キャッシュに保存される
    result = return_value(a)

    # 2度目の実行、キャッシュから取得される
    result = return_value(a)
    assert result == a, f"Failed for {a}"


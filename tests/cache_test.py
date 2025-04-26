import numpy as np
from mycache.array_db import load_array_from_db, save_array_to_db
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


def test_save_array_to_db():
    # NumPy配列を作成
    array = np.array(
        [
            [1.00001, 2.00001, 3.00001, 4.00001, 5.00001],
            [3.00001, 4.00001, 5.00001, 6.00001, 7.00001],
        ]
    )

    # 配列をデータベースに保存
    save_array_to_db("test_array", array)

    # データベースから配列を読み込む
    loaded_array = load_array_from_db("test_array")

    # 読み込んだ配列が元の配列と等しいことを確認
    assert np.shape(array) == np.shape(loaded_array), "Shape mismatch"
    assert np.array_equal(array, loaded_array), (
        "Loaded array does not match the original array"
    )

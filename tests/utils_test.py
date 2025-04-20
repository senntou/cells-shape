import numpy as np
import bisect

from utils import alter_points


def test_alter_points():
    points = [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5]]

    res = alter_points(points, NUM_POINTS=1000)
    answer = np.linspace(0, 5, num=1001)
    answer = np.column_stack((answer, answer))
    answer = answer[:-1]
    answer = np.append(answer, [answer[0]], axis=0)

    assert len(res) == len(answer), "Length of altered points is incorrect"
    assert np.allclose(res, answer), "Altered points do not match expected values"

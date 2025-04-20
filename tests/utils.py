import numpy as np

from util import alter_points


def test_alter_points():
    points = [[0, 0], [1, 1], [2, 0], [3, 1], [4, 0]]

    length = np.sum(np.linalg.norm(np.diff(points, axis=0), axis=1))

    assert length == 4.47213595499958, "Length calculation is incorrect"

    altered_points = alter_points(points)
    print("Altered Points: ", altered_points)

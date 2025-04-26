import numpy as np

from utils import alter_points


def test_alter_points():
    points = np.array([[1, 1], [-1, 1], [-1, -1], [1, -1]])
    expected = np.array(
        [[1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1], [1, 0]]
    )

    points = np.array(points)

    res = alter_points(points, num_points=8)

    assert len(res) == len(expected), "Length of altered points is incorrect"
    assert np.allclose(res, expected), "Altered points do not match expected values"

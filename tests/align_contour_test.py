import numpy as np
import matplotlib.pyplot as plt

from align import align_contour
from data.const import OUTPUT_TEST_PATH


def test_align_contour():
    length = 100
    contour_before = np.array(
        [
            [length, length],
            [-length, length],
            [-length, -length],
            [length, -length],
        ]
    )

    num_points = 20
    _, contour_after = align_contour(contour_before, num_points=num_points)

    assert len(contour_after) == num_points, "Number of points mismatch"

    contour_before = np.append(
        contour_before, [contour_before[0]], axis=0
    )  # 最初の点を追加

    # plot

    plt.figure()
    plt.plot(
        contour_before[:, 0], contour_before[:, 1], "ro-", label="Before", markersize=2
    )
    plt.plot(
        contour_after[:, 0], contour_after[:, 1], "bo-", label="After", markersize=2
    )
    plt.title("Contour Alignment Test")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.legend()
    plt.axis("equal")
    plt.grid()
    plt.savefig(f"{OUTPUT_TEST_PATH}/align_contour_test.png")

    plt.close()

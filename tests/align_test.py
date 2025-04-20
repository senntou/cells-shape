from types import new_class
from matplotlib.cbook import contiguous_regions
import numpy as np
import os
import matplotlib.pyplot as plt

from align import align_contour, calculate_polygon_centroid, calculate_principal_axes
from dio import get_json_data_from_number
from utils import alter_points

if not os.path.exists("output_test"):
    os.makedirs("output_test")


def test_align_contour():
    ids, contours = contour_data_provider()

    idx = 0
    for contour in contours:
        id = ids[idx]
        idx += 1
        aligned_contour = align_contour(contour)
        assert aligned_contour is not None, "整列された輪郭が計算されていません。"
        assert len(aligned_contour) == len(
            contour
        ), "整列された輪郭の長さがもとの輪郭と一致しません。"

        # contourとaligned_contourをグラフに描画
        plt.figure(figsize=(6, 6))
        plt.plot(
            contour[:, 0],
            contour[:, 1],
            marker="o",
            linestyle="-",
            color="blue",
            markersize=0,
        )
        plt.plot(
            aligned_contour[:, 0],
            aligned_contour[:, 1],
            marker="o",
            linestyle="-",
            color="red",
            markersize=0,
        )
        plt.title("Contour and Aligned Contour")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.grid(True)
        plt.axis("equal")  # 正方形スケールで表示
        plt.savefig(f"output_test/output_{id}.png", format="png")
        plt.close()


def test_calculate_polygon_centroid_convex():
    a = (1, 0)
    b = (1 / 2, np.sqrt(3) / 2)
    c = (-1 / 2, np.sqrt(3) / 2)
    d = (-1, 0)
    e = (-1 / 2, -np.sqrt(3) / 2)
    f = (1 / 2, -np.sqrt(3) / 2)

    vertices = np.array([a, b, c, d, e, f, a])

    centroid = calculate_polygon_centroid(vertices)

    assert centroid is not None, "重心が計算されていません。"
    assert np.allclose(centroid, (0, 0)), "重心の計算が正しくありません。"


def test_calculate_polygon_centroid_concave():
    a = (1, 0)
    b = (np.sqrt(3) / 4, 1 / 4)
    c = (1 / 2, np.sqrt(3) / 2)
    d = (0, 1 / 2)
    e = (-1 / 2, np.sqrt(3) / 2)
    f = (-np.sqrt(3) / 4, 1 / 4)
    g = (-1, 0)
    h = (-np.sqrt(3) / 4, -1 / 4)
    i = (-1 / 2, -np.sqrt(3) / 2)
    j = (0, -1 / 2)
    k = (1 / 2, -np.sqrt(3) / 2)
    l = (np.sqrt(3) / 4, -1 / 4)

    vertices = np.array([a, b, c, d, e, f, g, h, i, j, k, l, a])
    vertices += np.array((1, 1))

    centroid = calculate_polygon_centroid(vertices)

    assert centroid is not None, "重心が計算されていません。"
    assert np.allclose(centroid, (1, 1)), "重心の計算が正しくありません。"


def contour_data_provider():
    FILE_NUM = 0
    data = get_json_data_from_number(FILE_NUM)

    ids = ["7", "8", "9"]

    contours = []
    for id in ids:
        value = data["nuc"][id]
        points = value["contour"]
        points.append(points[0])
        points = np.array(points)
        points = alter_points(points)
        contours.append(points)

    return ids, contours


def test_calculate_principal_axes():
    contours = contour_data_provider()[1]
    contour = contours[1]

    v1, v2 = calculate_principal_axes(contour[:-1])

    mean = np.mean(contour[:-1], axis=0)

    plt.figure(figsize=(6, 6))
    plt.plot(
        contour[:, 0],
        contour[:, 1],
        marker="o",
        linestyle="-",
        color="blue",
        markersize=0,
    )

    v1 = v1 * 10
    v2 = v2 * 10

    # 主成分を直線で表示
    plt.plot(
        [mean[0] - v1[0], mean[0] + v1[0]],
        [mean[1] - v1[1], mean[1] + v1[1]],
        color="red",
        label="Principal Axis 1",
    )
    plt.plot(
        [mean[0] - v2[0], mean[0] + v2[0]],
        [mean[1] - v2[1], mean[1] + v2[1]],
        color="green",
        label="Principal Axis 2",
    )

    plt.title("Contour")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.axis("equal")  # 正方形スケールで表示
    plt.savefig(f"output_test/output_principal_axes.png", format="png")
    plt.close()

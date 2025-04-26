import numpy as np
import os
import matplotlib.pyplot as plt

from align import (
    align_contour,
    calculate_polygon_centroid,
    calculate_principal_axes,
    change_start_point,
    get_inside_points,
    insert_point_to_contour,
)
from data.const import OUTPUT_TEST_PATH
from data.dataio import get_json_data_from_number

if not os.path.exists("output"):
    os.makedirs("output")
if not os.path.exists(OUTPUT_TEST_PATH):
    os.makedirs(OUTPUT_TEST_PATH)


def test_align_contour():
    ids, contours = contour_data_provider()

    idx = 0
    for contour in contours:
        id = ids[idx]
        idx += 1
        aligned_contour, _ = align_contour(contour)

        assert aligned_contour is not None, "整列された輪郭が計算されていません。"
        assert type(aligned_contour) is np.ndarray, "整列された輪郭の型が不正です。"

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
        plt.savefig(f"{OUTPUT_TEST_PATH}/output_{id}.png", format="png")
        plt.close()


def test_calculate_polygon_centroid_convex():
    a = (1, 0)
    b = (1 / 2, np.sqrt(3) / 2)
    c = (-1 / 2, np.sqrt(3) / 2)
    d = (-1, 0)
    e = (-1 / 2, -np.sqrt(3) / 2)
    f = (1 / 2, -np.sqrt(3) / 2)

    vertices = np.array([a, b, c, d, e, f])

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

    vertices = np.array([a, b, c, d, e, f, g, h, i, j, k, l])
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
        points = np.array(points)
        contours.append(points)

    return ids, contours


# PCA
def test_calculate_principal_axes():
    ids, contours = contour_data_provider()

    idx = 0
    for contour in contours:
        id = ids[idx]
        idx += 1
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
        plt.savefig(f"{OUTPUT_TEST_PATH}/output_principal_axes_{id}.png", format="png")
        plt.close()


def test_get_inside_points_square():
    contour = np.array(
        [
            [0, 0],
            [1, 0],
            [1, 1],
            [0, 1],
        ]
    )

    inside_points = get_inside_points(contour, resolution=0.1)

    assert len(inside_points) > 0, "内側の点が見つかりません。"
    assert np.all(inside_points[:, 0] >= 0) and np.all(inside_points[:, 0] <= 1), (
        "X座標が範囲外です。"
    )
    assert np.all(inside_points[:, 1] >= 0) and np.all(inside_points[:, 1] <= 1), (
        "Y座標が範囲外です。"
    )

    contour = np.append(contour, [contour[0]], axis=0)  # 閉じるために最初の点を追加

    # グラフの作成
    plt.figure(figsize=(6, 6))
    plt.plot(
        contour[:, 0],
        contour[:, 1],
        marker="o",
        linestyle="-",
        color="blue",
        markersize=0,
    )
    plt.scatter(
        inside_points[:, 0],
        inside_points[:, 1],
        marker="o",
        color="red",
        s=10,
        label="Inside Points",
    )
    plt.title("Inside Points")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.axis("equal")  # 正方形スケールで表示
    plt.savefig(f"{OUTPUT_TEST_PATH}/output_inside_points_square.png", format="png")
    plt.close()


def test_get_inside_points_triangle():
    contour = np.array(
        [
            [0, 0],
            [1, 0],
            [0.5, np.sqrt(3) / 2],
        ]
    )

    inside_points = get_inside_points(contour, resolution=0.1)

    assert len(inside_points) > 0, "内側の点が見つかりません。"
    assert np.all(inside_points[:, 0] >= 0) and np.all(inside_points[:, 0] <= 1), (
        "X座標が範囲外です。"
    )
    assert np.all(inside_points[:, 1] >= 0) and np.all(
        inside_points[:, 1] <= np.sqrt(3) / 2
    ), "Y座標が範囲外です。"

    contour = np.append(contour, [contour[0]], axis=0)  # 閉じるために最初の点を追加

    # グラフの作成
    plt.figure(figsize=(6, 6))
    plt.plot(
        contour[:, 0],
        contour[:, 1],
        marker="o",
        linestyle="-",
        color="blue",
        markersize=0,
    )
    plt.scatter(
        inside_points[:, 0],
        inside_points[:, 1],
        marker="o",
        color="red",
        s=10,
        label="Inside Points",
    )
    plt.title("Inside Points")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.axis("equal")  # 正方形スケールで表示
    plt.savefig(f"{OUTPUT_TEST_PATH}/output_inside_points_triangle.png", format="png")
    plt.close()


def test_insert_point_to_contour():
    contour = np.array(
        [
            [1, 1],
            [-1, 1],
            [-1, -1],
            [1, -1],
            [1, 1],
        ]
    )

    excepted_contour = np.array(
        [
            [1, 1],
            [-1, 1],
            [-1, 0],
            [-1, -1],
            [1, -1],
            [1, 0],
            [1, 1],
        ]
    )

    res = insert_point_to_contour(contour)

    assert len(res) > len(contour), "新しい点が挿入されていません。"
    assert np.allclose(res, excepted_contour), "挿入された点が正しくありません。"


def test_change_start_point():
    contour = np.array(
        [
            [1, 1],
            [-1, 1],
            [-1, 0],
            [-1, -1],
            [1, -1],
            [1, 0],
        ]
    )

    excepted_contour = np.array(
        [
            [1, 0],
            [1, 1],
            [-1, 1],
            [-1, 0],
            [-1, -1],
            [1, -1],
        ]
    )

    res = change_start_point(contour)

    assert np.allclose(res, excepted_contour), "開始点が正しく変更されていません。"

import matplotlib.pyplot as plt
import numpy as np
import os
import bisect

from data.const import OUTPUT_CONTOUR_PATH, OUTPUT_OTHER_PATH

if not os.path.exists("output"):
    os.makedirs("output")
if not os.path.exists(OUTPUT_CONTOUR_PATH):
    os.makedirs(OUTPUT_CONTOUR_PATH)
if not os.path.exists(OUTPUT_OTHER_PATH):
    os.makedirs(OUTPUT_OTHER_PATH)


# points = [[x1, y1], [x2, y2], ..., [xn, yn]]
def create_svg(
    points: np.ndarray,
    id: str,
    path: str = OUTPUT_CONTOUR_PATH,
    show_number: bool = False,
) -> None:
    assert not np.allclose(points[0], points[-1]), "最初の点と最後の点が同じです"

    points = np.append(points, [points[0]], axis=0)  # 最初の点を最後に追加して閉じる

    x, y = zip(*points, strict=True)  # zip(*points)でx, yを分離

    # グラフの作成
    plt.figure(figsize=(6, 6))
    plt.plot(x, y, marker="o", linestyle="-", color="blue", markersize=0)

    # 番号を振ってラベルを表示
    if show_number:
        for i, (x_i, y_i) in enumerate(points):
            plt.text(x_i + 0.1, y_i + 0.1, str(i), fontsize=10, color="black")

    # 軸のラベルとグリッド（任意）
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.axis("equal")  # 正方形スケールで表示

    # SVG形式で保存（PDFにしたい場合は 'output.pdf' に変更）
    plt.savefig(f"{path}/output_" + id + ".svg", format="svg")
    plt.close()


# 点の取り方を変える
# points = [[x1, y1], [x2, y2], ..., [xn, yn]]
def alter_points(points: np.ndarray, num_points: int = 1000) -> np.ndarray:
    assert not np.allclose(points[0], points[-1]), "最初の点と最後の点が同じです"
    points = np.append(points, [points[0]], axis=0)  # 最初の点を最後に追加して閉じる

    # 1. 輪郭の長さを計算する
    # 2. 同時に各点までの始点からの距離を計算する
    # 3. 輪郭の長さをNUM_POINTSで割り，点を等間隔に配置する

    total_length = np.sum(np.linalg.norm(np.diff(points, axis=0), axis=1))

    # 各点までの始点からの距離を計算
    distances = np.zeros(len(points))
    for i in range(1, len(points)):
        distances[i] = distances[i - 1] + np.linalg.norm(
            np.array(points[i]) - np.array(points[i - 1])
        )

    # 各点の新しい位置を計算
    new_points = []
    for i in range(num_points):
        # 等間隔に配置するための距離
        dist = i * (total_length / num_points)

        # distance >= target_distance となる最小の点
        index = bisect.bisect_right(distances, dist) - 1
        assert 0 <= index < len(points) - 1, (
            "Index out of range" + "  i : " + str(i) + "  dist : " + str(dist)
        )

        # indexの点からindex+1の点の方向にdist - distances[index]だけ進む
        ratio = (dist - distances[index]) / np.linalg.norm(
            np.array(points[index + 1]) - np.array(points[index])
        )
        new_point = (
            points[index][0] + ratio * (points[index + 1][0] - points[index][0]),
            points[index][1] + ratio * (points[index + 1][1] - points[index][1]),
        )
        new_points.append(new_point)

    return np.array(new_points)


# 画像から見切れているかどうかを判定する
# points = [[x1, y1], [x2, y2], ..., [xn, yn], [x1, y1]]
def is_out_of_image(points: np.ndarray, image_size: tuple[int, int]) -> bool:
    # 画像のサイズを取得
    height, width = image_size
    margin = 0.001

    x_min = 0 + margin
    x_max = width - 1 - margin
    y_min = 0 + margin
    y_max = height - 1 - margin

    # 各点が画像の範囲内にあるかどうかをチェック
    for point in points:
        if not (x_min <= point[0] <= x_max and y_min <= point[1] <= y_max):
            return True  # 画像の範囲外にある点が見つかった
    return False  # すべての点が画像の範囲内にある


def plot_scatter(x: list[int], y: list[int], title: str = "") -> None:
    plt.scatter(x, y, s=4)
    plt.title(title)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.axis("equal")  # 正方形スケールで表示
    plt.savefig(f"{OUTPUT_OTHER_PATH}/" + title + ".svg", format="svg")


def eigenvec_subplot_each(
    x_mean: np.ndarray,
    eigenvectors: np.ndarray,
    weight: float,
    length: int = 13,
) -> None:
    for i in range(10):
        _, axes = plt.subplots(1, 3, figsize=(12, 4))
        for j in range(3):
            ax = axes[j]
            contour = (x_mean + eigenvectors[:, i] * (j - 1) * weight).reshape(-1, 2)
            ax.plot(
                contour[:, 0],
                contour[:, 1],
                "o",
                markersize=2,
            )
            ax.set_title(f"Eigenvector {i}: {(j - 1) * weight}")
            ax.set_xlim(-length, length)
            ax.set_ylim(-length, length)

        # レイアウトを調整
        plt.tight_layout()
        plt.savefig(OUTPUT_OTHER_PATH + f"/eigenvector_{i}_subplots.svg", format="svg")
        plt.close()


def eigenvec_subplot_2dim(
    mean: np.ndarray,
    eigenvectors_top2: np.ndarray,
    weight: float,
    length: int = 13,
) -> None:
    # 3x3のサブプロットを作成
    _, axes = plt.subplots(3, 3, figsize=(12, 12))

    # グラフを描画
    for i in range(3):
        for j in range(3):
            ax = axes[2 - j, i]

            contour = (
                mean
                + eigenvectors_top2 @ np.array([(i - 1) * weight, (j - 1) * weight])
            ).reshape(-1, 2)

            ax.plot(
                contour[:, 0],
                contour[:, 1],
                "o",
                markersize=2,
            )

            ax.set_title(f"PC1: {(i - 1) * weight}, PC2: {(j - 1) * weight}")

            ax.set_xlim(-length, length)
            ax.set_ylim(-length, length)

    # レイアウトを調整
    plt.tight_layout()
    plt.savefig(OUTPUT_OTHER_PATH + "/pca_scatter_subplots.svg", format="svg")
    plt.close()

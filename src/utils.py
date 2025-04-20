import matplotlib.pyplot as plt
import numpy as np
import os
import bisect

if not os.path.exists("output"):
    os.makedirs("output")


# points = [[x1, y1], [x2, y2], ..., [xn, yn], [x1, y1]]
def create_svg(points, id, show_number=False):
    x, y = zip(*points)

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
    plt.savefig("output/output_" + id + ".png", format="png")
    plt.close()


# 点の取り方を変える
# points = [[x1, y1], [x2, y2], ..., [xn, yn], [x1, y1]]
def alter_points(points, NUM_POINTS=1000):
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
    for i in range(NUM_POINTS):
        # 等間隔に配置するための距離
        dist = i * (total_length / NUM_POINTS)

        # distance >= target_distance となる最小の点
        index = bisect.bisect_right(distances, dist) - 1
        assert 0 <= index and index < len(points) - 1, (
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
def is_out_of_image(points, image_size):
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

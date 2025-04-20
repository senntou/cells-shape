from logging import logMultiprocessing
import matplotlib.pyplot as plt
import numpy as np
import os

if not os.path.exists("output"):
    os.makedirs("output")


# points = [[x1, y1], [x2, y2], ..., [xn, yn], [x1, y1]]
def create_svg(points, id):
    x, y = zip(*points)

    # グラフの作成
    plt.figure(figsize=(6, 6))
    plt.plot(x, y, marker="o", linestyle="-", color="blue")

    # 番号を振ってラベルを表示
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
def alter_points(points):
    # 1. 輪郭の長さを計算する
    # 2. 同時に各点までの始点からの距離を計算する
    # 3. 輪郭の長さをNUM_POINTSで割り，点を等間隔に配置する
    NUM_POINTS = 1000

    length = np.sum(np.linalg.norm(np.diff(points, axis=0), axis=1))

    print("length : ", length)

import matplotlib.pyplot as plt

# points = [(x1, y1), (x2, y2), ..., (xn, yn), (x1, y1)]
def create_svg(points, id):
    x, y = zip(*points)

    # グラフの作成
    plt.figure(figsize=(6, 6))
    plt.plot(x, y, marker='o', linestyle='-', color='blue')

    # 番号を振ってラベルを表示
    for i, (x_i, y_i) in enumerate(points):
        plt.text(x_i + 0.1, y_i + 0.1, str(i), fontsize=10, color='black')

    # 軸のラベルとグリッド（任意）
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)
    plt.axis('equal')  # 正方形スケールで表示

    # SVG形式で保存（PDFにしたい場合は 'output.pdf' に変更）
    plt.savefig("output/output_" + id + ".svg", format="svg")
    plt.close()

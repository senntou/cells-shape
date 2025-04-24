from calc import is_counter_clockwise
from align import align_contour
import numpy as np
import matplotlib.pyplot as plt

from data.const import OUTPUT_OTHER_PATH
from data.dataio import get_contours_from_all_files
from mycache.sqlite_cache import cache_to_sqlite
from mytypes.data_type import ContourData
from utils import create_svg, is_out_of_image, plot_scatter


# points = [[x1, y1], [x2, y2], ..., [xn, yn]]
def convert_points_format(points: list) -> np.ndarray:
    points.append(points[0])  # 閉じるために最初の点を追加
    return np.array(points)


@cache_to_sqlite
def get_contours_aligned(contours_data: dict[str, ContourData]) -> np.ndarray:
    contours = []
    contours_plane = []

    for key, value in contours_data.items():
        points = convert_points_format(value["contour"])
        img_size = value["img_size"]

        assert not is_counter_clockwise(points), (
            "key : " + key + " の観測点は反時計回りです"
        )

        if is_out_of_image(points, img_size):
            # print("key : ", key, " is out of image")
            continue

        contours_plane.append(points)  # 全体描画のため

        points, points_adjusted = align_contour(points)

        # create_svg(points, key, show_number=True)

        contours.append(points_adjusted)

    return np.array(contours)


def main() -> None:
    contours_data: dict[str, ContourData] = get_contours_from_all_files()

    print("合計データ数 : ", len(contours_data))
    contours_aligned = get_contours_aligned(contours_data)
    print("有効なデータ数 : ", len(contours_aligned))

    # 輪郭点の配列を1次元に変換
    x = contours_aligned.reshape(len(contours_aligned), -1)
    # 縦に1つのcontourが並ぶようにする
    x = x.T

    # 正規化
    x_normalized = x - np.mean(x, axis=1).reshape(-1, 1)

    # 分散共分散行列を計算
    covarience_matrix = np.cov(x_normalized)

    # 固有値と固有ベクトルを計算
    eigenvalues, eigenvectors = np.linalg.eigh(covarience_matrix)

    # 固有値の大きい順にソート
    sorted_indices = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[sorted_indices]
    eigenvectors = eigenvectors[:, sorted_indices]

    # 主成分得点を計算
    principal_components = np.dot(eigenvectors.T, x_normalized)

    # 主成分をプロット
    plot_scatter(
        principal_components[0, :],
        principal_components[1, :],
        "pca_scatter",
    )

    # 第i主成分をプロット
    for i in range(10):
        create_svg(
            eigenvectors[:, i].reshape(-1, 2),
            f"eigenvector_{i}",
            path=OUTPUT_OTHER_PATH,
            show_number=False,
        )

    x_mean = x.mean(axis=1)

    eigenvectors_top2 = eigenvectors[:, :2]

    # 第1, 第2主成分を調整しつつ、プロット
    weight = 30
    for i in range(-1, 2):
        for j in range(-1, 2):
            create_svg(
                (
                    x_mean + eigenvectors_top2 @ np.array([i * weight, j * weight])
                ).reshape(-1, 2),
                f"principal_components_{i * weight}_{j * weight}",
                path=OUTPUT_OTHER_PATH,
                show_number=False,
            )

    # 3x3のサブプロットを作成
    fig, axes = plt.subplots(3, 3, figsize=(12, 12))

    # グラフを描画
    for i in range(3):
        for j in range(3):
            # 各サブプロットにランダムなデータをプロット
            axes[2 - j, i].plot(
                (
                    x_mean
                    + eigenvectors_top2 @ np.array([(i - 1) * weight, (j - 1) * weight])
                ).reshape(-1, 2)[:, 0],
                (
                    x_mean
                    + eigenvectors_top2 @ np.array([(i - 1) * weight, (j - 1) * weight])
                ).reshape(-1, 2)[:, 1],
                "o",
                markersize=2,
            )
            axes[2 - j, i].set_title(
                f"PC1: {(i - 1) * weight}, PC2: {(j - 1) * weight}"
            )
            axes[2 - j, i].axis("equal")

    # レイアウトを調整
    plt.tight_layout()
    plt.savefig(OUTPUT_OTHER_PATH + "/pca_scatter_subplots.svg", format="svg")
    plt.close()

    for i in range(10):
        fig, axes = plt.subplots(1, 3, figsize=(12, 4))
        for j in range(3):
            # 各サブプロットにランダムなデータをプロット
            axes[j].plot(
                (x_mean + eigenvectors[:, i] * (j - 1) * weight).reshape(-1, 2)[:, 0],
                (x_mean + eigenvectors[:, i] * (j - 1) * weight).reshape(-1, 2)[:, 1],
                "o",
                markersize=2,
            )
            axes[j].set_title(f"Eigenvector {i}: {(j - 1) * weight}")
            axes[j].axis("equal")
        # レイアウトを調整
        plt.tight_layout()
        plt.savefig(OUTPUT_OTHER_PATH + f"/eigenvector_{i}_subplots.svg", format="svg")
        plt.close()


if __name__ == "__main__":
    main()
    # res = cProfile.run("main()", "profile.prof")
    # p = pstats.Stats("profile.prof")
    # p.strip_dirs().sort_stats("cumtime").print_stats(50)

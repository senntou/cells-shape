from calc import is_counter_clockwise
from align import align_contour
import numpy as np

from data.const import OUTPUT_OTHER_PATH
from data.dataio import get_contours_from_all_files
from mycache.array_db import save_array_to_db
from mycache.sqlite_cache import cache_to_sqlite
from mytypes.data_type import ContourData
from utils import (
    create_svg,
    eigenvec_subplot_2dim,
    eigenvec_subplot_each,
    is_out_of_image,
    plot_scatter,
)


# points = [[x1, y1], [x2, y2], ..., [xn, yn]]
def convert_points_format(points: list) -> np.ndarray:
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

        points, points_adjusted = align_contour(points, num_points=1000)

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

    weight = 30

    eigenvec_subplot_2dim(
        x_mean,
        eigenvectors_top2,
        weight,
    )

    eigenvec_subplot_each(
        x_mean,
        eigenvectors,
        weight,
    )

    save_array_to_db("mean", x_mean)
    save_array_to_db("eigenvectors", eigenvectors)


if __name__ == "__main__":
    main()
    # res = cProfile.run("main()", "profile.prof")
    # p = pstats.Stats("profile.prof")
    # p.strip_dirs().sort_stats("cumtime").print_stats(50)

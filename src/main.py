from matplotlib.pyplot import contour
from calc import is_counter_clockwise
from align import align_contour
import numpy as np

from data.dataio import get_contours_from_all_files
from mycache.sqlite_cache import cache_to_sqlite
from mytypes.data_type import ContourData
from utils import is_out_of_image


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


if __name__ == "__main__":
    main()
    # res = cProfile.run("main()", "profile.prof")
    # p = pstats.Stats("profile.prof")
    # p.strip_dirs().sort_stats("cumtime").print_stats(50)

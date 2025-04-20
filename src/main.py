import cProfile
from align import align_contour
from calc import is_counter_clockwise
from dio import get_json_data_from_number, draw_whole_image_with_contours
import numpy as np
import pstats

from image.size import get_image_size_from_file_number
from utils import alter_points, create_svg, is_out_of_image


# points = [[x1, y1], [x2, y2], ..., [xn, yn]]
def convert_points_format(points):
    points.append(points[0])  # 閉じるために最初の点を追加
    return np.array(points)


def main():
    FILE_NUM = 0
    data = get_json_data_from_number(FILE_NUM)
    img_size = get_image_size_from_file_number(FILE_NUM)

    # 総数を表示
    print("合計データ数 : ", len(data["nuc"]))

    cnt = 0

    contours = []
    contours_plane = []

    for key, value in data["nuc"].items():
        points = convert_points_format(value["contour"])

        assert is_counter_clockwise(points) == False, (
            "key : " + key + " の観測点は反時計回りです"
        )

        if is_out_of_image(points, img_size):
            print("key : ", key, " is out of image")
            continue

        contours_plane.append(points)  # 全体描画のため

        points, points_adjusted = align_contour(points)

        # create_svg(points, key, show_number=True)

        cnt += 1
        contours.append(points_adjusted)

    draw_whole_image_with_contours(FILE_NUM, contours_plane)

    print("有効なデータ数 : ", cnt)


if __name__ == "__main__":
    main()
    res = cProfile.run("main()", "profile.prof")
    p = pstats.Stats("profile.prof")
    p.strip_dirs().sort_stats("cumtime").print_stats(50)

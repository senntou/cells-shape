from calc import is_counter_clockwise
from dio import get_json_data_from_number
import numpy as np

from image.size import get_image_size_from_file_number
from utils import alter_points, create_svg, is_out_of_image


# points = [[x1, y1], [x2, y2], ..., [xn, yn]]
def convert_points_format(points):
    points.append(points[0])  # 閉じるために最初の点を追加
    return np.array(points)


if __name__ == "__main__":

    FILE_NUM = 0
    data = get_json_data_from_number(FILE_NUM)

    img_size = get_image_size_from_file_number(FILE_NUM)

    # 総数を表示
    print("合計データ数 : ", len(data["nuc"]))

    cnt = 0

    for key, value in data["nuc"].items():
        points = convert_points_format(value["contour"])

        if is_out_of_image(points, img_size):
            print("key : ", key, " is out of image")
            continue

        assert is_counter_clockwise(points) == False, (
            "key : " + key + " の観測点は反時計回りです"
        )

        points = alter_points(points)

        create_svg(points, key, show_number=False)

        cnt += 1

    print("有効なデータ数 : ", cnt)

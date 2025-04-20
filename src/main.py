from calc import is_counter_clockwise
from dio import get_json_data_from_number
import numpy as np

from util import create_svg

PATH = "/Dataset/Kurume_Dataset/Celltype_Dataset_v2/2024/2024_10_30/JSON/"


# points = [[x1, y1], [x2, y2], ..., [xn, yn]]
def convert_points_format(points):
    points.append(points[0])  # 閉じるために最初の点を追加
    return np.array(points)


if __name__ == "__main__":
    data = get_json_data_from_number(0)

    # 総数を表示
    print("count : ", len(data["nuc"]))

    cnt = 0

    for key, value in data["nuc"].items():
        points = convert_points_format(value["contour"])

        if is_counter_clockwise(points):
            print(f"{key} : counter-clockwise")

        create_svg(points, key)

        cnt += 1
        if cnt >= 10:
            break

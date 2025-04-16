import json

from calc import is_counter_clockwise
from util import create_svg

PATH = "/Dataset/Kurume_Dataset/Celltype_Dataset_v2/2024/2024_10_30/JSON/"


# データファイル名のリストを生成
file_names = []
for i in range(4, 14):
    file_names.append(f"kurume-policy_fl_c{i:03d}_v014.json")

# 1つ目のファイルのみを読み込む
with open( PATH + file_names[0], 'r', encoding='utf-8') as f:
    data = json.load(f)

# data["nuc"]に、辞書データが入っている
# コメントアウトを外すと、座標を表示して確認できる
# for key, value in data["nuc"].items():
#     print(value["contour"])

# 総数を表示
print("count : ", len(data["nuc"]))

for key, value in data["nuc"].items():
    points = []
    # x座標とy座標を取得
    contour = value["contour"]
    for point in contour:
        points.append((point[0], point[1]))
    points.append(points[0])  # 閉じるために最初の点を追加

    if is_counter_clockwise(points):
        print(f"{key} : counter-clockwise")

    create_svg(points, key)



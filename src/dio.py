import json
from PIL import Image, ImageDraw
import os

FILE_IDS = [i for i in range(4, 14)]

if not os.path.exists("output_whole"):
    os.makedirs("output_whole")


def get_file_names():
    file_names = []
    for i in FILE_IDS:
        file_names.append(f"kurume-policy_fl_c{i:03d}_v014.json")


def get_json_data_from_number(file_number):
    PATH = "/Dataset/Kurume_Dataset/Celltype_Dataset_v2/2024/2024_10_30/JSON/"
    id = FILE_IDS[file_number]
    file_name = f"kurume-policy_fl_c{id:03d}_v014.json"

    with open(PATH + file_name, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data


def get_tif_path_from_number(file_number):
    assert 0 <= file_number < len(FILE_IDS), "file_number is out of range"
    PATH = "/Dataset/Kurume_Dataset/Celltype_Dataset_v2/Image/"
    id = FILE_IDS[file_number]
    file_name = f"kurume-policy_fl_c{id:03d}_v001_he.tif"

    return PATH + file_name


# contoursは[[x1, y1], [x2, y2], ..., [xn, yn]]
def draw_whole_image_with_contours(file_number, contours):
    tif_path = get_tif_path_from_number(file_number)

    with Image.open(tif_path) as img:
        img = img.convert("RGB")  # RGBに変換
        draw = ImageDraw.Draw(img)

        for contour in contours:
            for i in range(len(contour) - 1):
                draw.line(
                    (
                        contour[i][0],
                        contour[i][1],
                        contour[i + 1][0],
                        contour[i + 1][1],
                    ),
                    fill=(255, 0, 0),
                    width=2,
                )

    img.save(f"output_whole/output_{file_number}.png")

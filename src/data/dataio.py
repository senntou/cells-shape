import json
from PIL import Image, ImageDraw
import os

from data.size import get_image_size_from_file_number
from data.const import FILE_IDS, JSON_PATH, get_tif_path_from_number
from mytypes.data_type import ContourData


if not os.path.exists("output_whole"):
    os.makedirs("output_whole")


def get_json_data_from_number(file_number: int) -> dict:
    id = FILE_IDS[file_number]
    file_name = f"kurume-policy_fl_c{id:03d}_v014.json"

    with open(JSON_PATH + file_name, encoding="utf-8") as f:
        data = json.load(f)

    return data


def get_contours_from_all_files() -> dict[str, ContourData]:
    contours_data: dict[str, ContourData] = {}

    for file_number in range(len(FILE_IDS)):
        json_data = get_json_data_from_number(file_number)
        img_size = get_image_size_from_file_number(file_number)

        for key, value in json_data["nuc"].items():
            new_key = f"{FILE_IDS[file_number]}_{key}"
            contours_data[new_key] = {
                "contour": value["contour"],
                "img_size": img_size,
            }

    return contours_data


# contoursは[[x1, y1], [x2, y2], ..., [xn, yn]]
def draw_whole_image_with_contours(
    file_number: int, contours: list[list[list[int]]]
) -> None:
    tif_path = get_tif_path_from_number(file_number)

    with Image.open(tif_path) as img:
        converted_img = img.convert("RGB")  # RGBに変換

        draw = ImageDraw.Draw(converted_img)

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

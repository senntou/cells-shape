FILE_IDS = [i for i in range(4, 14)]
JSON_PATH = "/Dataset/Kurume_Dataset/Celltype_Dataset_v2/2024/2024_10_30/JSON/"
IMAGE_PATH = "/Dataset/Kurume_Dataset/Celltype_Dataset_v2/Image/"

OUTPUT_CONTOUR_PATH = "output/contours"
OUTPUT_TEST_PATH = "output/test"
OUTPUT_OTHER_PATH = "output/other"


def get_file_names() -> list[str]:
    file_names = []
    for i in FILE_IDS:
        file_names.append(f"kurume-policy_fl_c{i:03d}_v014.json")

    return file_names


def get_tif_path_from_number(file_number: int) -> str:
    assert 0 <= file_number < len(FILE_IDS), "file_number is out of range"
    id = FILE_IDS[file_number]
    file_name = f"kurume-policy_fl_c{id:03d}_v001_he.tif"

    return IMAGE_PATH + file_name

import json


FILE_IDS = [i for i in range(4, 14)]


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

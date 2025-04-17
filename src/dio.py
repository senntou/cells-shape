
import json

PATH = "/Dataset/Kurume_Dataset/Celltype_Dataset_v2/2024/2024_10_30/JSON/"
file_ids = [i for i in range(4, 14)]

def get_file_names():
    file_names = []
    for i in file_ids:
        file_names.append(f"kurume-policy_fl_c{i:03d}_v014.json")

def get_json_data_from_number(file_number):
    id = file_ids[file_number]
    file_name = f"kurume-policy_fl_c{id:03d}_v014.json"
    
    with open(PATH + file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data

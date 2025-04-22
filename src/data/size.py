from PIL import Image

from data.const import get_tif_path_from_number


def get_image_size_from_file_number(file_number: int) -> tuple[int, int]:
    file_path = get_tif_path_from_number(file_number)

    with Image.open(file_path) as img:
        return img.size

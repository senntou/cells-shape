from image.size import get_image_size_from_file_number


def test_get_size_from_file_number():
    file_number = 0

    res = get_image_size_from_file_number(file_number)

    assert type(res) == tuple, "戻り値の型が不正です"

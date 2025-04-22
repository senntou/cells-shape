from typing import TypedDict


class ContourData(TypedDict):
    contour: list[list[int]]
    img_size: tuple[int, int]

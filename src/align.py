import numpy as np
from matplotlib.path import Path

from mycache.sqlite_cache import cache_to_sqlite
from calc import is_counter_clockwise
from utils import alter_points


# contour = [[x1, y1], [x2, y2], ..., [xn, yn], [x1, y1]]
def align_contour(
    contour: np.ndarray, num_points: int = 1000
) -> tuple[np.ndarray, np.ndarray]:
    assert not np.allclose(contour[0], contour[-1]), "輪郭が閉じています。"

    # 並進
    centroid = calculate_polygon_centroid(contour)
    new_contour = contour - centroid

    new_contour = np.append(new_contour, [new_contour[0]], axis=0)

    # 回転
    v1, v2 = calculate_principal_axes(new_contour[:-1])
    new_contour = np.dot(new_contour, np.array([v1, v2]).T)

    # 内挿
    new_contour = insert_point_to_contour(new_contour)

    # 点の追加
    new_contour_adjusted = alter_points(new_contour, num_points=num_points)

    # 裏表（上下）の判定・反転
    if is_reverse(new_contour_adjusted):
        new_contour = np.flipud(new_contour)
        new_contour_adjusted = np.flipud(new_contour_adjusted)

    # 反時計回りに並べ替え
    if not is_counter_clockwise(new_contour):
        new_contour = new_contour[::-1]
        new_contour_adjusted = new_contour_adjusted[::-1]

    # 始点を変更
    new_contour = change_start_point(new_contour[:-1])
    new_contour_adjusted = change_start_point(new_contour_adjusted[:-1])

    new_contour = np.array(new_contour)
    new_contour_adjusted = np.array(new_contour_adjusted)

    assert not np.allclose(new_contour[0], new_contour[-1]), (
        "調整された輪郭が閉じています。"
    )
    assert not np.allclose(new_contour_adjusted[0], new_contour_adjusted[-1]), (
        "調整された輪郭が閉じています。"
    )

    return new_contour, new_contour_adjusted


# vertices = [[x1, y1], [x2, y2], ..., [xn, yn]]
def calculate_polygon_centroid(vertices: np.ndarray) -> np.ndarray:
    assert not np.allclose(vertices[0], vertices[-1]), "頂点が閉じています。"

    vertices = np.append(vertices, [vertices[0]], axis=0)
    num_vertices = vertices.shape[0]

    # 頂点数が3未満の場合はエラーを返す(閉じているため、4以上)
    vertex_num = 3
    assert num_vertices >= vertex_num + 1, "多角形は3つ以上の頂点を持つ必要があります。"

    x = vertices[:, 0]
    y = vertices[:, 1]

    # 符号付き面積の計算
    signed_area = 0.5 * np.sum(x[:-1] * y[1:] - x[1:] * y[:-1])

    # 重心の計算
    centroid_x_numerator = np.sum((x[:-1] + x[1:]) * (x[:-1] * y[1:] - x[1:] * y[:-1]))
    centroid_y_numerator = np.sum((y[:-1] + y[1:]) * (x[:-1] * y[1:] - x[1:] * y[:-1]))

    centroid_x = centroid_x_numerator / (6 * signed_area)
    centroid_y = centroid_y_numerator / (6 * signed_area)

    return np.array([centroid_x, centroid_y])


# contour = [[x1, y1], [x2, y2], ..., [xn, yn]]
def get_inside_points(contour: np.ndarray, resolution: float = 1.0) -> np.ndarray:
    assert not np.allclose(contour[0], contour[-1]), "頂点が閉じています。"

    # 輪郭を囲む矩形を作成
    xmin, ymin = np.min(contour, axis=0)
    xmax, ymax = np.max(contour, axis=0)

    # 解像度に応じて格子点を作成
    x_grid = np.arange(xmin, xmax + resolution, resolution)
    y_grid = np.arange(ymin, ymax + resolution, resolution)
    xv, yv = np.meshgrid(x_grid, y_grid)
    grid_points = np.vstack((xv.ravel(), yv.ravel())).T

    # matplotlib.path.Pathで内外判定
    path = Path(contour)
    mask = path.contains_points(grid_points)
    inside_points = grid_points[mask]

    return inside_points


# PCAによって長軸と短軸を計算する
# contour = [[x1, y1], [x2, y2], ..., [xn, yn]]
def calculate_principal_axes(contour):
    assert not np.allclose(contour[0], contour[-1]), "頂点が閉じています。"

    # PCAを使用して主成分を計算
    contour = np.array(contour)
    points = get_inside_points(contour[:-1], resolution=0.5)
    mean = np.mean(points, axis=0)
    centered_points = points - mean

    covariance_matrix = np.cov(centered_points.T)
    eigenvalues, eigenvectors = np.linalg.eig(covariance_matrix)

    # 固有値の大きい順にソート
    sorted_indices = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[sorted_indices]
    eigenvectors = eigenvectors[:, sorted_indices]

    # 主成分の長軸と短軸を取得
    principal_axis_1 = eigenvectors[:, 0]
    principal_axis_2 = eigenvectors[:, 1]

    assert np.allclose(np.linalg.norm(principal_axis_1), 1), (
        f"主成分の長軸の長さが1ではありません。{np.linalg.norm(principal_axis_1)}"
    )
    assert np.allclose(np.linalg.norm(principal_axis_2), 1), (
        f"主成分の短軸の長さが1ではありません。{np.linalg.norm(principal_axis_2)}"
    )

    return principal_axis_1, principal_axis_2


# 輪郭がx軸と交わる場所に点を追加する
# contour = [[x1, y1], [x2, y2], ..., [xn, yn], [x1, y1]]
def insert_point_to_contour(contour: np.ndarray) -> np.ndarray:
    assert np.allclose(contour[0], contour[-1]), (
        "多角形の頂点は閉じている必要があります。"
    )

    new_contour = [contour[0]]  # 最初の点を追加

    for i in range(len(contour) - 1):
        p1 = contour[i]
        p2 = contour[i + 1]

        # x軸と交わる点を計算
        if (p1[1] > 0 and p2[1] < 0) or (p1[1] < 0 and p2[1] > 0):
            x_intersection = (p1[0] * p2[1] - p2[0] * p1[1]) / (p2[1] - p1[1])
            new_contour.append([x_intersection, 0])

        new_contour.append(p2)

    return np.array(new_contour)


# 形の上下を判定する
# 上側と下側の輪郭線の長さを比較する
# 既に等間隔に分割されていることを前提とする
# contour = [[x1, y1], [x2, y2], ..., [xn, yn], [x1, y1]]
def is_reverse(contour) -> bool:
    assert np.allclose(contour[0], contour[-1]), (
        "多角形の頂点は閉じている必要があります。"
    )
    # assert np.allclose(
    #     np.linalg.norm(contour[0] - contour[1]),
    #     np.linalg.norm(contour[-1] - contour[-2]),
    # ), "輪郭線の長さが等間隔ではありません。"

    # 上側と下側の輪郭点の数をカウント
    upper_count = np.sum(contour[:-1][:, 1] > 0)
    lower_count = np.sum(contour[:-1][:, 1] < 0)

    # 点の数が多いほうが上側
    # よって、上側の点の数が少ない場合は反転
    return upper_count < lower_count


# contour = [[x1, y1], [x2, y2], ..., [xn, yn]]
def change_start_point(contour):
    assert not np.allclose(contour[0], contour[-1]), "頂点が閉じていてはいけません。"

    # y = 0 のを点のうち、x座標が最大の点を探す
    idx = -1
    max_x = -np.inf
    for i in range(len(contour)):
        if np.isclose(contour[i][1], 0) and contour[i][0] > max_x:
            max_x = contour[i][0]
            idx = i

    # 新しい始点を設定
    new_contour = np.roll(contour, -idx, axis=0)

    return new_contour

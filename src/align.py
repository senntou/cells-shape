import numpy as np
import math


# contour = [[x1, y1], [x2, y2], ..., [xn, yn], [x1, y1]]
def align_contour(contour):
    assert np.allclose(
        contour[0], contour[-1]
    ), "多角形の頂点は閉じている必要があります。"

    centroid = calculate_polygon_centroid(contour)
    new_contour = contour - centroid

    v1, v2 = calculate_principal_axes(new_contour[:-1])
    new_contour = np.dot(new_contour, np.array([v1, v2]).T)

    return new_contour


# vertices = [[x1, y1], [x2, y2], ..., [xn, yn], [x1, y1]]
def calculate_polygon_centroid(vertices):
    assert np.allclose(
        vertices[0], vertices[-1]
    ), "多角形の頂点は閉じている必要があります。"

    vertices = np.array(vertices)
    num_vertices = vertices.shape[0]

    # 頂点数が3未満の場合はエラーを返す(閉じているため、4以上)
    assert num_vertices >= 4, "多角形は3つ以上の頂点を持つ必要があります。"

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


# PCAによって長軸と短軸を計算する
# points = [[x1, y1], [x2, y2], ..., [xn, yn]]
def calculate_principal_axes(points):
    assert not np.allclose(points[0], points[-1]), "頂点が閉じています。"

    # PCAを使用して主成分を計算
    points = np.array(points)
    mean = np.mean(points, axis=0)
    centered_points = points - mean

    covariance_matrix = np.cov(centered_points.T)
    _, eigenvectors = np.linalg.eig(covariance_matrix)

    # 主成分の長軸と短軸を取得
    principal_axis_1 = eigenvectors[:, 0]
    principal_axis_2 = eigenvectors[:, 1]

    assert np.allclose(
        np.linalg.norm(principal_axis_1), 1
    ), f"主成分の長軸の長さが1ではありません。{np.linalg.norm(principal_axis_1)}"
    assert np.allclose(
        np.linalg.norm(principal_axis_2), 1
    ), f"主成分の短軸の長さが1ではありません。{np.linalg.norm(principal_axis_2)}"

    return principal_axis_1, principal_axis_2

# points : [[x1, y1], [x2, y2], ..., [xn, yn], [x1, y1]]
def is_counter_clockwise(points):
    count = 0
    num = len(points) - 1  # 最初の点を追加しているので、-1する
    for i in range(num):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % num]
        x3, y3 = points[(i + 2) % num]
        # 3点の外積を計算
        vec1 = (x2 - x1, y2 - y1)
        vec2 = (x3 - x2, y3 - y2)
        cross_product = vec1[0] * vec2[1] - vec1[1] * vec2[0]
        if cross_product > 0:
            count += 1
        elif cross_product < 0:
            count -= 1

    # 外積が正の数が多い場合は反時計回り
    if count > 0:
        return True
    # 外積が負の数が多い場合は時計回り
    elif count < 0:
        return False

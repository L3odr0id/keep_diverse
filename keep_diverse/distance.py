def fast_distance(x_len: int, y_len: int, xy_len: int) -> float:
    return (xy_len - min(x_len, y_len)) / max(x_len, y_len)

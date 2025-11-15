def sort_tuple(data: list[tuple[int, str]]) -> list[tuple[int, str]]:
    return list(sorted(data, key=lambda x: x[0]))

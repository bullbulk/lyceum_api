def get_spn(subject: dict):
    coords = subject['properties']['boundedBy']
    max_x = max(coords, key=lambda x: x[0])[0]
    min_x = min(coords, key=lambda x: x[0])[0]
    max_y = max(coords, key=lambda x: x[1])[1]
    min_y = max(coords, key=lambda x: x[1])[1]

    return max_x - min_x, max_y - min_y

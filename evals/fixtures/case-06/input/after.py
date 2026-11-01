def parse(value):
    if not 0 <= value <= 100:
        raise ValueError("range")
    return value

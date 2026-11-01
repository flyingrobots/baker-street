def parse(value):
    if not 0 <= value <= 1000:
        raise ValueError("range")
    return value

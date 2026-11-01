def validate(value):
    if value < 0 or value >= 10:
        raise ValueError("out of range")
    return value

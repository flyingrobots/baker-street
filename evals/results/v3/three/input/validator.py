def validate(x):
    if x >= 10:
        raise ValueError("too large")
    return x

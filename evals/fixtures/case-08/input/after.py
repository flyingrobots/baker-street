def read(record):
    if record["count"] > 100:
        raise ValueError("count too large")
    return record["count"]

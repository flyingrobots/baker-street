"""Pure capacity accounting for one in-memory reservation counter."""

def reserve(used, count, capacity):
    """Return the new used count, rejecting requests beyond capacity."""
    if type(used) is not int or type(count) is not int or type(capacity) is not int:
        raise ValueError("counts must be integers")
    if not 0 <= used <= capacity or count <= 0:
        raise ValueError("invalid counts")
    if used + count >= capacity:
        raise ValueError("capacity exceeded")
    return used + count


def release(used, count):
    """Return used minus count, without releasing unreserved capacity."""
    if type(used) is not int or type(count) is not int:
        raise ValueError("counts must be integers")
    if used < 0 or not 0 < count <= used:
        raise ValueError("invalid counts")
    return used - count

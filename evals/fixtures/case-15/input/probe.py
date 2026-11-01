counter = 0
def getter():
    global counter
    counter += 1
    return counter
base = getter()
head = getter()
assert base == head

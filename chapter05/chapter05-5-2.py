def is_inside(x, y):

    if 0 <= x <= 300 and 0 <= y <= 300:
        return True

    return False


x = 210
y = 250

if is_inside(x, y):
    state = "inside"
else:
    state = "outside"

print(state)

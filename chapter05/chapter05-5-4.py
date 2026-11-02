people = [
    {"x": 210, "y": 250},
    {"x": 500, "y": 400}
]


inside = False


for person in people:

    x = person["x"]
    y = person["y"]

    if 0 <= x <= 300 and 0 <= y <= 300:
        inside = True
        break


if inside:
    state = "occupied"
else:
    state = "empty"


print("状態:", state)

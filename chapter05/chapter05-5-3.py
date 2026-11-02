people = [
    {"x": 210, "y": 250},
    {"x": 500, "y": 400}
]


for person in people:

    x = person["x"]
    y = person["y"]

    if 0 <= x <= 300 and 0 <= y <= 300:
        print("監視領域内")
    else:
        print("監視領域外")

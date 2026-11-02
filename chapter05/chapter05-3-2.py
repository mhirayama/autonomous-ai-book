people = [
    {"x": 210, "y": 250}
]

person_count = len(people)

if person_count == 0:
    state = "empty"
else:
    state = "occupied"

print("人数:", person_count)
print("状態:", state)
